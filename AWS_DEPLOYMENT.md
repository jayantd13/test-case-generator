# 🚀 AWS Deployment Guide for Test Case Generator

## 📋 Deployment Options

### Option 1: AWS EC2 (Recommended for teams)
- ✅ Full control over the environment
- ✅ Can run Ollama locally for free AI
- ✅ Cost-effective for continuous use
- ✅ Custom domain support

### Option 2: AWS App Runner
- ✅ Serverless, auto-scaling
- ✅ Easier deployment
- ✅ Pay per use
- ❌ Cannot run Ollama (need cloud AI)

### Option 3: AWS ECS Fargate
- ✅ Container-based deployment
- ✅ Auto-scaling
- ✅ Managed infrastructure
- ❌ More complex setup

### Option 4: AWS Lambda + API Gateway
- ✅ Serverless, very cost-effective
- ✅ Pay only when used
- ❌ 15-minute execution limit
- ❌ Complex for Streamlit

## 🏆 Recommended: AWS EC2 Deployment

### Prerequisites
- AWS Account
- Basic AWS knowledge
- SSH client (PuTTY for Windows)

---

## 🚀 OPTION 1: AWS EC2 Step-by-Step

### Step 1: Launch EC2 Instance

1. **Login to AWS Console**
2. **Go to EC2 Dashboard**
3. **Click "Launch Instance"**
4. **Configure:**
   - **Name**: `testcase-generator`
   - **AMI**: Ubuntu Server 22.04 LTS
   - **Instance type**: `t3.medium` (2 vCPU, 4GB RAM)
   - **Key pair**: Create new or use existing
   - **Security group**: Allow HTTP (80), HTTPS (443), SSH (22), Custom (8501)
   - **Storage**: 20GB gp3

### Step 2: Connect to Instance

```bash
# Connect via SSH
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### Step 3: Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv nginx -y

# Install Git
sudo apt install git -y

# Install Ollama (for free AI)
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
sudo systemctl enable ollama
sudo systemctl start ollama

# Download AI model
ollama pull llama3.2
```

### Step 4: Deploy Application

```bash
# Clone your project
git clone <your-repo-url> /home/ubuntu/testcase-generator
# OR upload files via SCP/SFTP

cd /home/ubuntu/testcase-generator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your settings
nano .env
```

### Step 5: Configure for Production

```bash
# Create systemd service
sudo nano /etc/systemd/system/testcase-generator.service
```

Add this content:
```ini
[Unit]
Description=Test Case Generator Streamlit App
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/testcase-generator
Environment=PATH=/home/ubuntu/testcase-generator/venv/bin
ExecStart=/home/ubuntu/testcase-generator/venv/bin/streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable testcase-generator
sudo systemctl start testcase-generator
```

### Step 6: Configure Nginx Reverse Proxy

```bash
# Create Nginx config
sudo nano /etc/nginx/sites-available/testcase-generator
```

Add this content:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain or EC2 public IP

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/testcase-generator /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

### Step 7: Access Your Application

- **URL**: `http://your-ec2-public-ip`
- **Or**: `http://your-domain.com` (if you have a domain)

---

## 🚀 OPTION 2: AWS App Runner (Simpler)

### Step 1: Prepare for App Runner

Create `apprunner.yaml`:
```yaml
version: 1.0
runtime: python3
build:
  commands:
    build:
      - echo "Installing dependencies"
      - pip install -r requirements.txt
run:
  runtime-version: 3.11
  command: streamlit run streamlit_app.py --server.port=8080 --server.address=0.0.0.0
  network:
    port: 8080
    env: PORT
  env:
    - name: DEFAULT_AI_PROVIDER
      value: groq
```

### Step 2: Deploy to App Runner

1. **Go to AWS App Runner Console**
2. **Create new service**
3. **Source**: Repository (GitHub) or ECR
4. **Upload your code**
5. **Configure environment variables**
6. **Deploy**

---

## 🚀 OPTION 3: Docker + ECS (Advanced)

### Step 1: Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Step 2: Build and Push to ECR

```bash
# Build image
docker build -t testcase-generator .

# Tag for ECR
docker tag testcase-generator:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/testcase-generator:latest

# Push to ECR
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/testcase-generator:latest
```

### Step 3: Deploy to ECS

Create ECS task definition and service using AWS Console or CLI.

---

## 🔧 Environment Variables for AWS

Update your `.env` for production:

```env
# AI Provider Configuration
DEFAULT_AI_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here

# For Ollama on EC2
OLLAMA_BASE_URL=http://localhost:11434

# Production settings
DEFAULT_TEST_TYPE=Functional
DEFAULT_COMPONENT=Web Application
DEFAULT_RELEASE=1.0
DEFAULT_TEST_STATUS=Draft
DEFAULT_AUTOMATION_STATUS=Not Automated

# Security (for production)
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true
```

---

## 🔒 Security Considerations

### 1. Security Groups
```
- Port 22 (SSH): Your IP only
- Port 80 (HTTP): 0.0.0.0/0
- Port 443 (HTTPS): 0.0.0.0/0
- Port 8501: localhost only (behind Nginx)
```

### 2. SSL Certificate (Optional)
```bash
# Install Certbot for free SSL
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### 3. Firewall
```bash
# Configure UFW
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

---

## 💰 Cost Estimation

### EC2 t3.medium (recommended)
- **Instance**: ~$30/month
- **Storage**: ~$2/month
- **Data transfer**: ~$5-10/month
- **Total**: ~$40-45/month

### App Runner
- **Pay per use**: ~$0.064/hour when running
- **Scaling**: Automatic
- **Total**: Varies based on usage

---

## 🚀 Quick Deployment Script

Save as `deploy.sh`:

```bash
#!/bin/bash
echo "🚀 Deploying Test Case Generator to AWS EC2"

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3 python3-pip python3-venv nginx git -y

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl enable ollama
sudo systemctl start ollama
ollama pull llama3.2

# Setup application
cd /home/ubuntu
git clone https://github.com/your-repo/testcase-generator.git
cd testcase-generator

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
echo "Please edit .env file with your API keys"

# Start services
sudo systemctl start testcase-generator
sudo systemctl enable testcase-generator

echo "✅ Deployment complete!"
echo "Access your app at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
```

## 🎯 Recommended Approach

For your use case, I recommend **AWS EC2** because:
1. ✅ You can run Ollama locally (free AI)
2. ✅ Full control over the environment
3. ✅ Cost-effective for team usage
4. ✅ Easy to maintain and update

Would you like me to help you with any specific deployment option?
