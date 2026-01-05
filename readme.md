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

---

### CloudWatch Logs

| Log Source | Purpose |
|----------|---------|
| **Flask Application Logs** | Tracks backend requests, errors, and application behavior |
| **Lambda Execution Logs** | Captures event processing and notification workflow details |

---

### CloudWatch Alarms

| Alarm | Trigger Condition |
|------|-------------------|
| **High CPU Usage** | Alerts when CPU utilization exceeds safe threshold |
| **Instance Status Check Failures** | Detects EC2 system or instance-level failures |

---

## Setup & Deployment (High Level)

- Launch Amazon EC2 (Amazon Linux)  
- Install Python, Nginx, and required dependencies  
- Clone project to `/usr/share/nginx/html/cloudvault`  
- Create and activate Python virtual environment  
- Install Python dependencies  
- Configure IAM roles and permissions  
- Configure Nginx reverse proxy  
- Start Flask application  
- Configure S3, RDS, Lambda, SNS, and CloudWatch 

---

## Real-World Problems Solved

- AWS Signature Version 4 upload issues  
- Flask static asset resolution  
- Nginx reverse proxy errors  
- Virtual environment dependency isolation  
- IAM permission misconfigurations  
- Secure direct-to-S3 upload patterns  

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