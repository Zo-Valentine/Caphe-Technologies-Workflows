# 🚀 Quick Reference - AWS EC2 Deployment

## Initial Deployment

```bash
# 1. SSH into EC2
ssh -i "vscode.pem" ec2-user@ec2-44-220-54-182.compute-1.amazonaws.com

# 2. Download deployment script
curl -O https://raw.githubusercontent.com/Zo-Valentine/caphe-n8n-workflows/master/deploy-to-ec2.sh

# 3. Run deployment
chmod +x deploy-to-ec2.sh && ./deploy-to-ec2.sh
```

## Update Existing Deployment

```bash
# Download and run update script
curl -O https://raw.githubusercontent.com/Zo-Valentine/caphe-n8n-workflows/master/update-deployment.sh
chmod +x update-deployment.sh && ./update-deployment.sh
```

## Common Commands

### Container Management
```bash
docker logs -f caphe-workflows           # View logs
docker restart caphe-workflows           # Restart
docker stop caphe-workflows              # Stop
docker start caphe-workflows             # Start
docker exec -it caphe-workflows bash     # Shell access
```

### Quick Fixes
```bash
# Restart container
docker restart caphe-workflows

# Rebuild and restart
docker stop caphe-workflows
docker rm caphe-workflows
cd caphe-n8n-workflows/frameworks/caphe-workflows
docker build -t caphe-workflows:latest .
docker run -d --name caphe-workflows --restart always -p 8000:8000 \
  -v $(pwd)/database:/app/database \
  -v $(pwd)/workflows:/app/workflows \
  --env-file .env caphe-workflows:latest

# Check status
docker ps | grep caphe-workflows
```

### Backup & Restore
```bash
# Create backup
cd ~/caphe-n8n-workflows/frameworks/caphe-workflows
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz database/ workflows/ .env

# Restore backup
docker stop caphe-workflows
tar -xzf backup_XXXXXXXX_XXXXXX.tar.gz
docker start caphe-workflows
```

## Access Application

```
http://YOUR-EC2-PUBLIC-IP:8000
```

## Troubleshooting

```bash
# View logs
docker logs caphe-workflows

# Check resources
docker stats caphe-workflows

# Clean Docker
docker system prune -f

# Rebuild from scratch
docker stop caphe-workflows && docker rm caphe-workflows
cd ~/caphe-n8n-workflows/frameworks/caphe-workflows
docker build --no-cache -t caphe-workflows:latest .
docker run -d --name caphe-workflows --restart always -p 8000:8000 \
  -v $(pwd)/database:/app/database \
  -v $(pwd)/workflows:/app/workflows \
  --env-file .env caphe-workflows:latest
```

## Security Group Ports

- **SSH**: Port 22 (from your IP)
- **HTTP**: Port 8000 (from 0.0.0.0/0 or restricted)

## Files Location

```
~/caphe-n8n-workflows/frameworks/caphe-workflows/
├── database/          # SQLite database
├── workflows/         # Workflow files
├── logs/             # Application logs
├── backups/          # Backup files
└── .env              # Environment config
```
