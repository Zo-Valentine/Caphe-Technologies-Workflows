#!/bin/bash

################################################################################
# Caphe Workflows - AWS EC2 Deployment Script
# This script automates the deployment of Caphe Workflows to an EC2 instance
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="https://github.com/Zo-Valentine/Caphe-Technologies-Workflows.git"
PROJECT_DIR="Caphe-Technologies-Workflows"
APP_DIR="frameworks/caphe-workflows"
CONTAINER_NAME="caphe-workflows"
IMAGE_NAME="caphe-workflows"
PORT=8000

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo ""
    echo -e "${BLUE}============================================================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}============================================================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

check_command() {
    if command -v $1 &> /dev/null; then
        print_success "$1 is installed"
        return 0
    else
        print_error "$1 is not installed"
        return 1
    fi
}

################################################################################
# Installation Steps
################################################################################

install_docker() {
    print_header "Installing Docker"
    
    if check_command docker; then
        print_info "Docker is already installed"
        docker --version
    else
        print_info "Installing Docker..."
        sudo yum update -y
        sudo yum install docker -y
        sudo service docker start
        sudo systemctl enable docker
        sudo usermod -a -G docker $USER
        print_success "Docker installed successfully"
        
        print_info "Please log out and log back in, or run: newgrp docker"
        print_info "Then re-run this script"
        exit 0
    fi
}

install_docker_compose() {
    print_header "Installing Docker Compose"
    
    if check_command docker-compose; then
        print_info "Docker Compose is already installed"
        docker-compose --version
    else
        print_info "Installing Docker Compose..."
        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
        print_success "Docker Compose installed successfully"
        docker-compose --version
    fi
}

install_git() {
    print_header "Installing Git"
    
    if check_command git; then
        print_info "Git is already installed"
        git --version
    else
        print_info "Installing Git..."
        sudo yum install git -y
        print_success "Git installed successfully"
        git --version
    fi
}

clone_repository() {
    print_header "Cloning Repository"
    
    if [ -d "$PROJECT_DIR" ]; then
        print_info "Repository already exists. Pulling latest changes..."
        cd $PROJECT_DIR
        git pull
        cd ..
    else
        print_info "Cloning repository from $REPO_URL"
        git clone $REPO_URL
        print_success "Repository cloned successfully"
    fi
}

setup_environment() {
    print_header "Setting Up Environment"
    
    cd $PROJECT_DIR/$APP_DIR
    
    if [ -f ".env" ]; then
        print_info "Environment file already exists"
    else
        print_info "Creating production environment file..."
        cat > .env << 'EOF'
# Production Environment Configuration
ENVIRONMENT=production
LOG_LEVEL=info
ENABLE_METRICS=true
MAX_WORKERS=4
PORT=8000
HOST=0.0.0.0

# Database Configuration (if needed)
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=caphe_workflows
# DB_USER=admin
# DB_PASSWORD=change_this_password

# Security (generate your own secrets)
# SECRET_KEY=your-secret-key-here
# JWT_SECRET=your-jwt-secret-here

# Optional: External Services
# SMTP_HOST=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USER=your-email@gmail.com
# SMTP_PASSWORD=your-app-password
EOF
        print_success "Environment file created"
        print_info "Please review and update .env file with your configuration"
    fi
    
    cd - > /dev/null
}

create_directories() {
    print_header "Creating Required Directories"
    
    cd $PROJECT_DIR/$APP_DIR
    
    mkdir -p database workflows logs backups
    print_success "Directories created: database, workflows, logs, backups"
    
    cd - > /dev/null
}

build_and_run() {
    print_header "Building and Running Docker Container"
    
    cd $PROJECT_DIR/$APP_DIR
    
    # Stop and remove existing container if running
    if [ "$(docker ps -a -q -f name=$CONTAINER_NAME)" ]; then
        print_info "Stopping existing container..."
        docker stop $CONTAINER_NAME || true
        docker rm $CONTAINER_NAME || true
    fi
    
    # Remove old image if exists
    if [ "$(docker images -q $IMAGE_NAME)" ]; then
        print_info "Removing old image..."
        docker rmi $IMAGE_NAME || true
    fi
    
    print_info "Building Docker image..."
    docker build -t $IMAGE_NAME:latest .
    print_success "Docker image built successfully"
    
    print_info "Starting container..."
    docker run -d \
        --name $CONTAINER_NAME \
        --restart always \
        -p $PORT:$PORT \
        -v $(pwd)/database:/app/database \
        -v $(pwd)/workflows:/app/workflows \
        -v $(pwd)/logs:/app/logs \
        --env-file .env \
        $IMAGE_NAME:latest
    
    print_success "Container started successfully"
    
    cd - > /dev/null
}

check_container_status() {
    print_header "Container Status"
    
    print_info "Waiting for container to start..."
    sleep 5
    
    if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
        print_success "Container is running!"
        echo ""
        docker ps -f name=$CONTAINER_NAME
        echo ""
        print_info "Viewing container logs (press Ctrl+C to exit)..."
        echo ""
        docker logs -f --tail 50 $CONTAINER_NAME
    else
        print_error "Container failed to start"
        print_info "Checking logs..."
        docker logs $CONTAINER_NAME
        exit 1
    fi
}

display_access_info() {
    print_header "Deployment Successful!"
    
    # Get public IP
    PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 || echo "your-ec2-ip")
    
    echo ""
    print_success "Caphe Workflows is now running!"
    echo ""
    echo -e "${GREEN}Access your application at:${NC}"
    echo -e "${BLUE}  http://$PUBLIC_IP:$PORT${NC}"
    echo ""
    echo -e "${YELLOW}Useful Commands:${NC}"
    echo "  View logs:        docker logs -f $CONTAINER_NAME"
    echo "  Stop container:   docker stop $CONTAINER_NAME"
    echo "  Start container:  docker start $CONTAINER_NAME"
    echo "  Restart:          docker restart $CONTAINER_NAME"
    echo "  Shell access:     docker exec -it $CONTAINER_NAME bash"
    echo "  Container stats:  docker stats $CONTAINER_NAME"
    echo ""
    echo -e "${YELLOW}Important Security Notes:${NC}"
    echo "  1. Update your EC2 Security Group to allow inbound traffic on port $PORT"
    echo "  2. Review and update the .env file with secure passwords"
    echo "  3. Consider setting up SSL/TLS with a reverse proxy (nginx/traefik)"
    echo "  4. Set up regular backups of the database and workflows directories"
    echo ""
}

################################################################################
# Main Execution
################################################################################

main() {
    print_header "Caphe Workflows - AWS EC2 Deployment"
    
    echo "This script will:"
    echo "  1. Install Docker and Docker Compose"
    echo "  2. Install Git"
    echo "  3. Clone the repository"
    echo "  4. Set up environment configuration"
    echo "  5. Build and run the Docker container"
    echo ""
    
    read -p "Do you want to continue? (y/n) " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Deployment cancelled"
        exit 0
    fi
    
    # Execute deployment steps
    install_docker
    install_docker_compose
    install_git
    clone_repository
    setup_environment
    create_directories
    build_and_run
    
    # Wait a moment before checking status
    sleep 3
    
    display_access_info
}

# Run main function
main "$@"
