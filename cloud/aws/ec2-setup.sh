#!/bin/bash
# cloud/aws/ec2-setup.sh
# Run once after launching your AWS EC2 Ubuntu 22.04 instance

sudo apt-get update -y
sudo apt-get install -y docker.io docker-compose git python3-pip

sudo systemctl start docker
sudo usermod -aG docker ubuntu

# Clone project
git clone https://github.com/YOUR_USERNAME/freshness-classifier.git
cd freshness-classifier

# Start app
docker-compose up -d

echo "✅ App is running at http://$(curl -s ifconfig.me):5000"
