import boto3
import json

ec2 = boto3.client('ec2', region_name='ap-south-1')

user_data_script = """#!/bin/bash
yum update -y
yum install -y python3 python3-pip git
pip3 install fastapi uvicorn transformers torch --index-url https://download.pytorch.org/whl/cpu
echo "FastAPI environment ready"
"""

print("AWS Deployment Configuration:")
print(json.dumps({
    "service": "EC2 t2.micro",
    "region": "ap-south-1 (Mumbai)",
    "instance_type": "t2.micro",
    "free_tier": True,
    "port": 8000,
    "model": "DistilBERT Fake News Classifier v1.0",
    "estimated_monthly_cost": "$0 (within free tier limits)"
}, indent=2))

print("\nDeployment architecture:")
print("User Request → EC2 Instance → FastAPI → DistilBERT Model → Response")