import boto3
import os

# AWS S3 Configuration
S3_BUCKET = "snowflake-web-app"
CONFIG_FILE = "config.json"
LOCAL_CONFIG_PATH = "C:\\Users\\JAYARAMAGUDIPATI\\Documents\\snowflake_web_app"

# Download configuration file from S3
def download_config():
    s3 = boto3.client('s3')
    s3.download_file(S3_BUCKET, CONFIG_FILE, LOCAL_CONFIG_PATH)
    print(f"✅ Config file downloaded from S3: {LOCAL_CONFIG_PATH}")

# Run Docker container with environment variables
def run_container():
    os.system("docker build -t snowflake-app .")
    os.system("docker run -p 5000:5000 --env-file /tmp/config.json snowflake-app")

if __name__ == "__main__":
    download_config()
    run_container()
