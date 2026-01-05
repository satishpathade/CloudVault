import boto3
from botocore.config import Config
from config import S3_BUCKET, UPLOAD_URL_EXPIRY

# MUST match bucket region exactly
S3_REGION = "ap-south-1"   # change ONLY if your bucket is in another region

s3_client = boto3.client(
    "s3",
    region_name=S3_REGION,
    config=Config(
        signature_version="s3v4",
        s3={"addressing_style": "virtual"}
    )
)

def generate_presigned_upload_url(object_key: str) -> str:
    return s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": S3_BUCKET,
            "Key": object_key
        },
        ExpiresIn=UPLOAD_URL_EXPIRY
    )
