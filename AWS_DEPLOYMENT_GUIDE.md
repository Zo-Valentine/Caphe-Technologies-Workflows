# AWS EC2 Deployment Guide for Caphe Workflows

This guide provides comprehensive instructions for deploying Caphe Workflows to an AWS EC2 instance using Docker.

## 📋 Prerequisites

Before you begin, ensure you have:

1. **AWS Account** - Active AWS account with permissions to create EC2 instances
2. **EC2 Instance** - Running EC2 instance (Amazon Linux 2 or Amazon Linux 2023 recommended)
3. **SSH Access** - SSH key pair (`.pem` file) to access your EC2 instance
4. **Security Group** - Configured to allow:
   - SSH (port 22) from your IP
   - HTTP (port 8000) from anywhere (or restricted as needed)

## 🚀 Quick Start

### 1. Connect to Your EC2 Instance

```bash
# Set correct permissions on your SSH key
chmod 600 vscode.pem

# SSH into your EC2 instance
ssh -i "vscode.pem" ec2-user@ec2-44-220-54-182.compute-1.amazonaws.com
```

### 2. Download and Run the Deployment Script

Once connected to your EC2 instance:

```bash
# Download the deployment script
curl -O https://raw.githubusercontent.com/Zo-Valentine/caphe-n8n-workflows/master/deploy-to-ec2.sh

# Make it executable
chmod +x deploy-to-ec2.sh

# Run the deployment
./deploy-to-ec2.sh
```

The script will automatically:
- ✅ Install Docker and Docker Compose
- ✅ Install Git
- ✅ Clone your repository
- ✅ Set up environment configuration
- ✅ Build the Docker image
- ✅ Start the container
- ✅ Display access information

### 3. Access Your Application

After successful deployment, access your application at:
```
http://YOUR-EC2-PUBLIC-IP:8000
```

## 🔄 Updating Your Deployment

To update your deployment with the latest code:

```bash
# Download the update script
curl -O https://raw.githubusercontent.com/Zo-Valentine/caphe-n8n-workflows/master/update-deployment.sh

# Make it executable
chmod +x update-deployment.sh

# Run the update
./update-deployment.sh
```

The update script will:
- ✅ Create a backup of your current deployment
- ✅ Pull the latest code
- ✅ Rebuild the Docker image
- ✅ Restart the container with zero downtime (as much as possible)
- ✅ Verify the deployment

## 📁 Manual Deployment Steps

If you prefer to deploy manually, follow these steps:

### Step 1: Install Docker

```bash
# Update system packages
sudo yum update -y

# Install Docker
sudo yum install docker -y

# Start Docker service
sudo service docker start
sudo systemctl enable docker

# Add user to docker group
sudo usermod -a -G docker ec2-user

# Apply group changes
newgrp docker
```

### Step 2: Install Docker Compose

```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version
```

### Step 3: Install Git

```bash
sudo yum install git -y
```

### Step 4: Clone Repository

```bash
git clone https://github.com/Zo-Valentine/caphe-n8n-workflows.git
cd caphe-n8n-workflows/frameworks/caphe-workflows
```

### Step 5: Configure Environment

```bash
# Create .env file
cat > .env << 'EOF'
ENVIRONMENT=production
LOG_LEVEL=info
ENABLE_METRICS=true
MAX_WORKERS=4
PORT=8000
HOST=0.0.0.0
EOF

# Create required directories
mkdir -p database workflows logs backups
```

### Step 6: Build and Run

```bash
# Build Docker image
docker build -t caphe-workflows:latest .

# Run container
docker run -d \
  --name caphe-workflows \
  --restart always \
  -p 8000:8000 \
  -v $(pwd)/database:/app/database \
  -v $(pwd)/workflows:/app/workflows \
  -v $(pwd)/logs:/app/logs \
  --env-file .env \
  caphe-workflows:latest

# Check status
docker ps

# View logs
docker logs -f caphe-workflows
```

## 🛠️ Useful Commands

### Container Management

```bash
# View logs
docker logs -f caphe-workflows

# Stop container
docker stop caphe-workflows

# Start container
docker start caphe-workflows

# Restart container
docker restart caphe-workflows

# Access container shell
docker exec -it caphe-workflows bash

# View container stats
docker stats caphe-workflows

# Remove container
docker rm -f caphe-workflows
```

### Image Management

```bash
# List images
docker images

# Remove old images
docker image prune -f

# Rebuild image
docker build --no-cache -t caphe-workflows:latest .
```

### System Maintenance

```bash
# View disk usage
docker system df

# Clean up everything
docker system prune -a

# View running containers
docker ps

# View all containers
docker ps -a
```

## 🔒 Security Configuration

### 1. Configure EC2 Security Group

In AWS Console:
1. Go to EC2 Dashboard
2. Select your instance
3. Click on "Security Groups"
4. Add inbound rules:
   - Type: SSH, Port: 22, Source: Your IP
   - Type: Custom TCP, Port: 8000, Source: 0.0.0.0/0 (or restrict as needed)

### 2. Update Environment Variables

Edit the `.env` file to add secure passwords and secrets:

```bash
cd ~/caphe-n8n-workflows/frameworks/caphe-workflows
nano .env
```

Update with secure values:
```env
SECRET_KEY=generate-a-random-secret-key-here
JWT_SECRET=generate-another-random-secret-here
DB_PASSWORD=use-a-strong-database-password
```

### 3. Set Up SSL/TLS (Recommended for Production)

For production deployments, set up a reverse proxy with SSL:

```bash
# Install nginx
sudo yum install nginx -y

# Configure nginx as reverse proxy
sudo nano /etc/nginx/conf.d/caphe-workflows.conf
```

Add configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📊 Monitoring and Logs

### View Application Logs

```bash
# Real-time logs
docker logs -f caphe-workflows

# Last 100 lines
docker logs --tail 100 caphe-workflows

# Logs with timestamps
docker logs -t caphe-workflows
```

### Monitor Resource Usage

```bash
# Container stats
docker stats caphe-workflows

# System resources
htop  # Install with: sudo yum install htop -y
```

### Log Files Location

Logs are stored in the mounted volume:
```bash
cd ~/caphe-n8n-workflows/frameworks/caphe-workflows/logs
tail -f application.log
```

## 🔄 Backup and Recovery

### Create Manual Backup

```bash
cd ~/caphe-n8n-workflows/frameworks/caphe-workflows

# Create backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
tar -czf backup_$TIMESTAMP.tar.gz database/ workflows/ .env

# Store backup safely
mkdir -p backups
mv backup_$TIMESTAMP.tar.gz backups/
```

### Restore from Backup

```bash
cd ~/caphe-n8n-workflows/frameworks/caphe-workflows

# Stop container
docker stop caphe-workflows

# Restore backup
tar -xzf backups/backup_XXXXXXXX_XXXXXX.tar.gz

# Restart container
docker start caphe-workflows
```

### Automated Backup Script

```bash
# Create backup script
cat > ~/backup.sh << 'EOF'
#!/bin/bash
cd ~/caphe-n8n-workflows/frameworks/caphe-workflows
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
tar -czf backups/backup_$TIMESTAMP.tar.gz database/ workflows/ .env
# Keep only last 7 backups
ls -t backups/backup_*.tar.gz | tail -n +8 | xargs -r rm
EOF

chmod +x ~/backup.sh

# Add to crontab for daily backups at 2 AM
(crontab -l 2>/dev/null; echo "0 2 * * * ~/backup.sh") | crontab -
```

## 🐛 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs caphe-workflows

# Check if port is already in use
sudo netstat -tlnp | grep 8000

# Rebuild image
docker build --no-cache -t caphe-workflows:latest .
docker stop caphe-workflows
docker rm caphe-workflows
docker run -d --name caphe-workflows -p 8000:8000 caphe-workflows:latest
```

### Permission Issues

```bash
# Fix ownership
cd ~/caphe-n8n-workflows/frameworks/caphe-workflows
sudo chown -R ec2-user:ec2-user .

# Fix Docker permissions
sudo usermod -a -G docker ec2-user
newgrp docker
```

### Database Issues

```bash
# Access container
docker exec -it caphe-workflows bash

# Check database
cd /app/database
ls -la

# Run database reindex
python run.py --reindex
```

### Out of Disk Space

```bash
# Check disk usage
df -h

# Clean up Docker
docker system prune -a -f

# Clean up logs
sudo journalctl --vacuum-time=7d
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [GitHub Repository](https://github.com/Zo-Valentine/caphe-n8n-workflows)

## 🆘 Support

If you encounter issues:

1. Check the logs: `docker logs caphe-workflows`
2. Verify environment configuration: `cat .env`
3. Check system resources: `docker stats`
4. Review security group settings in AWS Console
5. Create an issue on GitHub with error details

## 📝 License

This project is licensed under the terms specified in the repository.

---

**Last Updated:** November 24, 2025
