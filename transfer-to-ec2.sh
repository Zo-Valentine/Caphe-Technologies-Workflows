#!/bin/bash

################################################################################
# Transfer Deployment Scripts to EC2 Instance
# This script copies the deployment scripts from your local machine to EC2
################################################################################

# Configuration
EC2_USER="ec2-user"
EC2_HOST="ec2-44-220-54-182.compute-1.amazonaws.com"
SSH_KEY="vscode.pem"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Transferring deployment scripts to EC2 instance...${NC}"
echo ""

# Ensure SSH key has correct permissions
chmod 600 "$SSH_KEY"

# Transfer deployment script
echo "📤 Transferring deploy-to-ec2.sh..."
scp -i "$SSH_KEY" deploy-to-ec2.sh ${EC2_USER}@${EC2_HOST}:~/
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ deploy-to-ec2.sh transferred successfully${NC}"
else
    echo "❌ Failed to transfer deploy-to-ec2.sh"
    exit 1
fi

# Transfer update script
echo "📤 Transferring update-deployment.sh..."
scp -i "$SSH_KEY" update-deployment.sh ${EC2_USER}@${EC2_HOST}:~/
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ update-deployment.sh transferred successfully${NC}"
else
    echo "❌ Failed to transfer update-deployment.sh"
    exit 1
fi

echo ""
echo -e "${GREEN}✓ All files transferred successfully!${NC}"
echo ""
echo "Next steps:"
echo "1. SSH into your EC2 instance:"
echo "   ssh -i \"$SSH_KEY\" ${EC2_USER}@${EC2_HOST}"
echo ""
echo "2. Run the deployment script:"
echo "   chmod +x deploy-to-ec2.sh"
echo "   ./deploy-to-ec2.sh"
echo ""
