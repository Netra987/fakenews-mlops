# AWS Deployment Plan — Fake News Detector

## Region
ap-south-1 (Mumbai) — chosen for lowest latency from India

## Architecture
User → Internet → EC2 t2.micro → FastAPI (port 8000) → DistilBERT Model

## Services Used
- EC2 t2.micro — hosts the FastAPI application (free tier: 750 hrs/month)
- S3 — stores model artifacts and DVC data (free tier: 5GB)
- CloudWatch — monitors CPU, memory, API response times
- IAM — manages access control with least privilege policy

## Deployment Steps
1. Launch EC2 t2.micro with Amazon Linux 2
2. SSH into instance and install Python, FastAPI, transformers
3. Copy model files from S3 to EC2
4. Run uvicorn on port 8000
5. Configure security group to allow inbound port 8000
6. Set up CloudWatch alarm for CPU > 80%

## Cost Estimate
- EC2 t2.micro: $0/month (free tier)
- S3 5GB: $0/month (free tier)
- CloudWatch basic: $0/month (free tier)
- Total: $0 within free tier limits

## IAM Policy Applied
- AmazonEC2FullAccess
- AmazonS3FullAccess
- Principle of least privilege followed

## Why Mumbai Region
- Lowest latency for Indian users (~10ms vs ~150ms for US regions)
- Compliant with Indian data residency preferences
- Same AWS infrastructure quality as other regions