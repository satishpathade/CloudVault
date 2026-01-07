# CloudVault – Secure File Upload & Storage System (AWS)

CloudVault is a real-world AWS cloud storage application designed with security, scalability, cost optimization, and monitoring in mind.

---

## Features

- Secure browser-based uploads using **Amazon S3 pre-signed URLs**
- File deletion synchronized across S3 and database
- Event-driven upload notifications (S3 → Lambda → SNS)
- Storage cost optimization using S3 lifecycle rules
- Centralized logging and monitoring with CloudWatch
- IAM role–based security (no hardcoded credentials)

---

## Architecture

CloudVault follows a stateless, event-driven AWS architecture:

## End-to-End Flow

![Architecture-flow](<architecture/CloudVault – Full Architecture Flow.png>)

---

## Tech Stack

### Backend

| Technology | Purpose |
|-----------|---------|
| **Python 3** | Core backend programming language |
| **Flask** | Web framework for API handling and routing |
| **boto3** | AWS SDK for interacting with S3, SNS, and other AWS services |
| **pymysql** | MySQL client library for Amazon RDS connectivity |

### Frontend

| Technology | Purpose |
|-----------|---------|
| **HTML** | Structure of the user interface |
| **CSS** | Styling and layout for the application UI |
| **JavaScript (Vanilla)** | Client-side logic for uploads, gallery view, and interactions |

## AWS Services

| AWS Service | Purpose in Project |
|------------|-------------------|
| **Amazon EC2 (Amazon Linux)** | Hosts the Flask backend and Nginx reverse proxy |
| **Nginx** | Acts as a reverse proxy to route HTTP traffic to the Flask application |
| **Amazon S3** | Stores uploaded files securely using pre-signed URLs |
| **Amazon RDS (MySQL)** | Stores file metadata such as filename, folder, type, and object key |
| **AWS Lambda** | Triggered by S3 events to process upload notifications |
| **Amazon SNS** | Sends email notifications on successful file uploads and alerts |
| **Amazon CloudWatch** | Monitors logs, metrics, and triggers alarms for system health |
| **IAM Roles** | Provides secure, least-privilege access to AWS services without access keys |


---

## Project Structure 

```
cloudvault/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   └── upload_routes.py
│   ├── services/
│   │   ├── s3_service.py
│   │   ├── db_service.py
│   │   └── notification_service.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── app.js
│       └── styles.css
│
├── config.py
├── run.py
├── requirements.txt
├── venv/
├── architecture/
│   ├── architecture\CloudVault – Full Architecture Flow.png
│   └── 
└── README.md
```
---

## Security

- No AWS credentials stored in code  
- EC2 and Lambda use IAM roles  
- Least-privilege IAM permissions enforced  
- S3 public access fully blocked  
- Uploads allowed only via pre-signed URLs  

---


## Storage Optimization - S3 Lifecycle Rules

S3 lifecycle configuration:

- **Day 0–29** → S3 Standard  
- **Day 30–59** → S3 Standard-IA  
- **Day 60+** → Glacier Flexible Retrieval  

S3 versioning is enabled to protect against accidental deletion or overwrite.

---

## Monitoring & Alerts

Notifications are delivered using **Amazon SNS**.

### CloudWatch Metrics

| Metric | Purpose |
|------|---------|
| **EC2 CPU Utilization** | Monitors server load and detects performance spikes |

### CloudWatch Logs

| Log Source | Purpose |
|----------|---------|
| **Flask Application Logs** | Tracks backend requests, errors, and application behavior |
| **Lambda Execution Logs** | Captures event processing and notification workflow details |

### CloudWatch Alarms

| Alarm | Trigger Condition |
|------|-------------------|
| **High CPU Usage** | Alerts when CPU utilization exceeds safe threshold |
| **Instance Status Check Failures** | Detects EC2 system or instance-level failures |

---

## Setup & Deployment (High Level)

- Launch Amazon EC2 (Amazon Linux)
    ### Security Group Rules
    | Type | Protocol | Port | Source |
    |----|----|----|----|
    | SSH | TCP | 22 | Your IP |
    | HTTP | TCP | 80 | 0.0.0.0/0 |

- Connect to EC2 & Install System Dependencies
    ```
    sudo yum update -y
    sudo yum install -y python3 python3-pip nginx git
    ```
- Clone Project into Nginx Web Root 
    ```
    cd /usr/share/nginx/html
    sudo git clone https://github.com/satishpathade/CloudVault.git
    sudo chown -R ec2-user:ec2-user CloudVault
    cd CloudVault
    ```

- Create and activate Python virtual environment 
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```

- Install Python dependencies  
    ```
    pip install --upgrade pip
    pip install -r requirements.txt
    ```
    
- Configure IAM roles and permissions  
- Configure Nginx reverse proxy  
    ```
    sudo nano /etc/nginx/nginx.confi
    server {
        listen 80;
        server_name _;

        location / {
            proxy_pass http://127.0.0.1:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
    ```
- Start Flask application  
    ```
    source venv/bin/activate
    nohup python run.py > app.log 2>&1 &
    ```
- Configure S3

    ### Bucket Details
    - **Bucket Name**: `cloudvault-files-uploads`
    - **Region**: `ap-south-1`
    - **Purpose**: Store uploaded files securely

    ### Configuration Steps
    - Block **all public access**
    - Enable **Bucket Versioning**

    ### Lifecycle Rules (Cost Optimization)

    | Age of Object | Storage Class |
    |--------------|---------------|
    | Day 0–29 | S3 Standard |
    | Day 30–59 | S3 Standard-IA |
    | Day 60+ | Glacier Flexible Retrieval |

    This ensures long-term storage cost optimization.

- RDS

    ## 🗄️ Amazon RDS (MySQL) Configuration

    ### Database Details
    - **DB Identifier**: `cloudvault-db`
    - **Engine**: MySQL
    - **DB Name**: `cloudvault`
    - **Username**: `root`
    - **Access**: Private (not publicly accessible)

    ### Security
    - RDS Security Group allows inbound MySQL (3306) **only from EC2 security group**

    ### Table Schema

    ```sql
    CREATE TABLE file_metadata (
        id INT AUTO_INCREMENT PRIMARY KEY,
        original_filename VARCHAR(255),
        s3_object_key VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ```

- AWS Lambda
    AWS Lambda is used to implement an event-driven workflow for file upload notifications

    ### Lambda Function Details

    | Property | Value |
    |--------|-------|
    | **Function Name** | `cloudvault-s3-upload-notifier` |
    | **Runtime** | Python 3.10 |
    | **Trigger Source** | Amazon S3 |
    | **Trigger Event** | `ObjectCreated` |
    | **Purpose** | Process S3 upload events and initiate notifications |

- SNS Topic Details

    | Property | Value |
    |--------|-------|
    | **Topic Name** | `cloudvault-cpu-alerts` |
    | **Topic Name** | `cloudvault-upload-events`|
    | **Protocol** | Email |
    | **Purpose** | Notify users or administrators of successful file uploads |

- Amazon CloudWatch  

    Amazon CloudWatch provides monitoring, logging, and alerting for the CloudVault system.

    ### CloudWatch Metrics

    | Metric | Description |
    |------|-------------|
    | **EC2 CPU Utilization** | Monitors backend server load |
    | **Instance Health Status** | Tracks EC2 system and instance checks |

    ### CloudWatch Logs

    | Log Source | Purpose |
    |----------|---------|
    | **Flask Application Logs** | Monitor backend requests and errors |
    | **Lambda Execution Logs** | Debug event processing and notifications |

    ### CloudWatch Alarms

    | Alarm Name | Trigger Condition |
    |-----------|------------------|
    | `cloudvault-cpu-high` | CPU Utilization > 60% |

Alarm notifications are sent using **Amazon SNS** to ensure rapid response to system issues.

---

## Future Enhancements

- User authentication and private folders  
- HTTPS using ALB or Let’s Encrypt  
- Secure file downloads via pre-signed URLs  
- Nested folder support  
- CI/CD pipeline using GitHub Actions  
- CloudFront CDN for faster image delivery 

---

## Author

**Satish Pathade**   
Focused on building reliable, scalable, production-ready systems on AWS.
