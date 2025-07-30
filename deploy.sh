#!/bin/bash

# 🚀 AWS EC2 Deployment Script for Test Case Generator
# Run this script on a fresh Ubuntu 22.04 EC2 instance

set -e  # Exit on any error

echo "🚀 Starting deployment of Test Case Generator..."
echo "=================================================="

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "📦 Installing Python, Nginx, and Git..."
sudo apt install -y python3 python3-pip python3-venv nginx git curl

# Install Ollama for local AI (optional but recommended)
echo "🤖 Installing Ollama for local AI..."
curl -fsSL https://ollama.com/install.sh | sh

# Configure Ollama as a service
echo "⚙️ Configuring Ollama service..."
sudo systemctl enable ollama
sudo systemctl start ollama

# Wait for Ollama to start
sleep 5

# Download AI model
echo "📥 Downloading AI model (this may take a few minutes)..."
ollama pull llama3.2

# Create application directory
echo "📁 Setting up application directory..."
APP_DIR="/home/ubuntu/testcase-generator"
sudo mkdir -p $APP_DIR
sudo chown ubuntu:ubuntu $APP_DIR

# Copy application files (assuming they're already uploaded)
cd $APP_DIR

# Create Python virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Set up environment file
echo "⚙️ Configuring environment..."
if [ ! -f .env ]; then
    cp .env .env.backup 2>/dev/null || true
    cat > .env << EOF
# Test Case Generator Configuration

# AI Provider (ollama is running locally)
DEFAULT_AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434

# Default settings
DEFAULT_MODEL=llama3.2
DEFAULT_TEST_TYPE=Functional
DEFAULT_COMPONENT=Web Application
DEFAULT_RELEASE=1.0
DEFAULT_TEST_STATUS=Draft
DEFAULT_AUTOMATION_STATUS=Not Automated

# Streamlit settings for production
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true
EOF
fi

# Create systemd service for the application
echo "🔧 Creating systemd service..."
sudo tee /etc/systemd/system/testcase-generator.service > /dev/null << EOF
[Unit]
Description=Test Case Generator Streamlit App
After=network.target ollama.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
ExecStart=$APP_DIR/venv/bin/streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
echo "🚀 Starting Test Case Generator service..."
sudo systemctl daemon-reload
sudo systemctl enable testcase-generator
sudo systemctl start testcase-generator

# Configure Nginx reverse proxy
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/testcase-generator > /dev/null << EOF
server {
    listen 80;
    server_name _;  # Replace with your domain if you have one

    client_max_body_size 50M;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        proxy_read_timeout 86400;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://localhost:8501/_stcore/health;
    }
}
EOF

# Enable the Nginx site
sudo ln -sf /etc/nginx/sites-available/testcase-generator /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx

# Configure firewall
echo "🔒 Configuring firewall..."
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

# Get public IP
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)

echo ""
echo "🎉 Deployment completed successfully!"
echo "=================================================="
echo ""
echo "✅ Services Status:"
echo "   - Ollama: $(sudo systemctl is-active ollama)"
echo "   - Test Case Generator: $(sudo systemctl is-active testcase-generator)"
echo "   - Nginx: $(sudo systemctl is-active nginx)"
echo ""
echo "🌐 Access your application at:"
echo "   http://$PUBLIC_IP"
echo ""
echo "📋 Useful commands:"
echo "   sudo systemctl status testcase-generator  # Check app status"
echo "   sudo systemctl logs -f testcase-generator # View app logs"
echo "   sudo systemctl restart testcase-generator # Restart app"
echo "   ollama list                               # List AI models"
echo ""
echo "🔧 To add SSL certificate:"
echo "   sudo apt install certbot python3-certbot-nginx"
echo "   sudo certbot --nginx -d yourdomain.com"
echo ""

# Check if services are running
sleep 10
if sudo systemctl is-active --quiet testcase-generator; then
    echo "✅ Test Case Generator is running successfully!"
else
    echo "❌ Test Case Generator failed to start. Check logs:"
    echo "   sudo systemctl status testcase-generator"
    echo "   sudo journalctl -u testcase-generator -f"
fi
