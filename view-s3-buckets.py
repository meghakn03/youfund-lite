import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1",
)

# List buckets
buckets = s3.list_buckets()
print("Buckets:")
for bucket in buckets.get("Buckets", []):
    print(f" - {bucket['Name']}")

# List objects in a specific bucket
bucket_name = "your-bucket-name"
objects = s3.list_objects_v2(Bucket=bucket_name)
print(f"Objects in bucket {bucket_name}:")
for obj in objects.get("Contents", []):
    print(f" - {obj['Key']}")
