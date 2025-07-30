#!/bin/bash

# 🧪 Quick AWS ECS Deployment Script
# This script creates all necessary AWS resources for ECS deployment

set -e

# Configuration
CLUSTER_NAME="testcase-generator-cluster"
SERVICE_NAME="testcase-generator-service"
TASK_NAME="testcase-generator-task"
REGION="us-east-1"
ECR_REPO="testcase-generator"

echo "🚀 Deploying Test Case Generator to AWS ECS"
echo "============================================="

# Check if AWS CLI is configured
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "❌ AWS CLI not configured. Please run 'aws configure' first."
    exit 1
fi

# Get AWS Account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_URI="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$ECR_REPO"

echo "📋 Configuration:"
echo "   Account ID: $ACCOUNT_ID"
echo "   Region: $REGION"
echo "   ECR Repository: $ECR_URI"
echo ""

# Create ECR repository
echo "📦 Creating ECR repository..."
aws ecr create-repository --repository-name $ECR_REPO --region $REGION 2>/dev/null || echo "Repository already exists"

# Get ECR login token
echo "🔐 Logging into ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_URI

# Build Docker image
echo "🏗️ Building Docker image..."
docker build -t $ECR_REPO .

# Tag image for ECR
docker tag $ECR_REPO:latest $ECR_URI:latest

# Push image to ECR
echo "📤 Pushing image to ECR..."
docker push $ECR_URI:latest

# Create ECS cluster
echo "🏗️ Creating ECS cluster..."
aws ecs create-cluster --cluster-name $CLUSTER_NAME --region $REGION 2>/dev/null || echo "Cluster already exists"

# Create task definition
echo "📋 Creating task definition..."
cat > task-definition.json << EOF
{
    "family": "$TASK_NAME",
    "networkMode": "awsvpc",
    "requiresCompatibilities": ["FARGATE"],
    "cpu": "512",
    "memory": "1024",
    "executionRoleArn": "arn:aws:iam::$ACCOUNT_ID:role/ecsTaskExecutionRole",
    "containerDefinitions": [
        {
            "name": "testcase-generator",
            "image": "$ECR_URI:latest",
            "portMappings": [
                {
                    "containerPort": 8501,
                    "protocol": "tcp"
                }
            ],
            "essential": true,
            "environment": [
                {
                    "name": "DEFAULT_AI_PROVIDER",
                    "value": "groq"
                },
                {
                    "name": "DEFAULT_MODEL",
                    "value": "llama3-8b-8192"
                }
            ],
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/ecs/$TASK_NAME",
                    "awslogs-region": "$REGION",
                    "awslogs-stream-prefix": "ecs"
                }
            }
        }
    ]
}
EOF

# Create CloudWatch log group
aws logs create-log-group --log-group-name "/ecs/$TASK_NAME" --region $REGION 2>/dev/null || echo "Log group already exists"

# Register task definition
echo "📝 Registering task definition..."
aws ecs register-task-definition --cli-input-json file://task-definition.json --region $REGION

# Get default VPC and subnets
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=is-default,Values=true" --query "Vpcs[0].VpcId" --output text --region $REGION)
SUBNET_IDS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query "Subnets[*].SubnetId" --output text --region $REGION)
SUBNET_1=$(echo $SUBNET_IDS | cut -d' ' -f1)
SUBNET_2=$(echo $SUBNET_IDS | cut -d' ' -f2)

# Create security group
echo "🔒 Creating security group..."
SG_ID=$(aws ec2 create-security-group \
    --group-name testcase-generator-sg \
    --description "Security group for Test Case Generator" \
    --vpc-id $VPC_ID \
    --region $REGION \
    --query 'GroupId' \
    --output text 2>/dev/null || \
    aws ec2 describe-security-groups \
    --filters "Name=group-name,Values=testcase-generator-sg" \
    --query "SecurityGroups[0].GroupId" \
    --output text \
    --region $REGION)

# Allow HTTP traffic
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 8501 \
    --cidr 0.0.0.0/0 \
    --region $REGION 2>/dev/null || echo "Security group rule already exists"

# Create ECS service
echo "🚀 Creating ECS service..."
aws ecs create-service \
    --cluster $CLUSTER_NAME \
    --service-name $SERVICE_NAME \
    --task-definition $TASK_NAME \
    --desired-count 1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_1,$SUBNET_2],securityGroups=[$SG_ID],assignPublicIp=ENABLED}" \
    --region $REGION 2>/dev/null || echo "Service already exists"

# Wait for service to be running
echo "⏳ Waiting for service to start..."
aws ecs wait services-running --cluster $CLUSTER_NAME --services $SERVICE_NAME --region $REGION

# Get the public IP
echo "🔍 Getting public IP address..."
TASK_ARN=$(aws ecs list-tasks --cluster $CLUSTER_NAME --service-name $SERVICE_NAME --query "taskArns[0]" --output text --region $REGION)
ENI_ID=$(aws ecs describe-tasks --cluster $CLUSTER_NAME --tasks $TASK_ARN --query "tasks[0].attachments[0].details[?name=='networkInterfaceId'].value" --output text --region $REGION)
PUBLIC_IP=$(aws ec2 describe-network-interfaces --network-interface-ids $ENI_ID --query "NetworkInterfaces[0].Association.PublicIp" --output text --region $REGION)

echo ""
echo "🎉 Deployment completed successfully!"
echo "====================================="
echo ""
echo "✅ Service Status: Running"
echo "🌐 Access your application at: http://$PUBLIC_IP:8501"
echo "📊 ECS Console: https://console.aws.amazon.com/ecs/home?region=$REGION#/clusters/$CLUSTER_NAME/services"
echo ""
echo "📋 Useful commands:"
echo "   aws ecs describe-services --cluster $CLUSTER_NAME --services $SERVICE_NAME --region $REGION"
echo "   aws logs tail /ecs/$TASK_NAME --follow --region $REGION"
echo ""
echo "🗑️ To clean up resources:"
echo "   aws ecs update-service --cluster $CLUSTER_NAME --service $SERVICE_NAME --desired-count 0 --region $REGION"
echo "   aws ecs delete-service --cluster $CLUSTER_NAME --service $SERVICE_NAME --region $REGION"
echo "   aws ecs delete-cluster --cluster $CLUSTER_NAME --region $REGION"

# Clean up temporary files
rm -f task-definition.json
