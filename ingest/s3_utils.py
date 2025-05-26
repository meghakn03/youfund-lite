# ingest/s3_utils.py
import boto3
from io import BytesIO, StringIO
import pandas as pd

# S3 client pointing at LocalStack
_s3 = boto3.client(
    "s3",
    endpoint_url="http://localstack:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1",
)

def ensure_bucket_exists(bucket: str):
    existing_buckets = _s3.list_buckets()
    if not any(b['Name'] == bucket for b in existing_buckets['Buckets']):
        _s3.create_bucket(Bucket=bucket)

def upload_df(df: pd.DataFrame, bucket: str, key: str):
    ensure_bucket_exists(bucket)
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    _s3.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())


def download_df(bucket: str, key: str) -> pd.DataFrame:
    resp = _s3.get_object(Bucket=bucket, Key=key)
    return pd.read_csv(BytesIO(resp["Body"].read()))
