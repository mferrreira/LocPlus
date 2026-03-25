import os
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from fastapi import UploadFile, HTTPException

MINIO_INTERNAL_URL = os.getenv("MINIO_INTERNAL_URL", "http://minio:9000") # Comunicação interna docker-to-docker
MINIO_PUBLIC_URL = os.getenv("MINIO_PUBLIC_URL", "http://localhost:9000") # URL pública que o React vai visualizar
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minio_admin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minio_senha_segura")
BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "locplus-vistorias")

s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_INTERNAL_URL,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1"
)

def ensure_bucket_exists():
    try:
        s3_client.head_bucket(Bucket=BUCKET_NAME)
    except ClientError:
        try:
            s3_client.create_bucket(Bucket=BUCKET_NAME)
            policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": ["s3:GetObject"],
                        "Resource": [f"arn:aws:s3:::{BUCKET_NAME}/*"]
                    }
                ]
            }
            import json
            s3_client.put_bucket_policy(Bucket=BUCKET_NAME, Policy=json.dumps(policy))
        except Exception as e:
            print(f"Erro ao criar bucket {BUCKET_NAME}: {e}")

ensure_bucket_exists()

def upload_file_to_minio(file: UploadFile, object_name: str) -> str:
    try:
        s3_client.upload_fileobj(
            file.file,
            BUCKET_NAME,
            object_name,
            ExtraArgs={"ContentType": file.content_type}
        )
        return f"{MINIO_PUBLIC_URL}/{BUCKET_NAME}/{object_name}"
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Erro no S3/MinIO: {str(e)}")
