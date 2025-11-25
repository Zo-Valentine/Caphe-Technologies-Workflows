#!/bin/bash

################################################################################
# Caphe Workflows - Update Script
# This script updates an existing deployment with the latest changes
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="Caphe-Technologies-Workflows"
APP_DIR="frameworks/caphe-workflows"
CONTAINER_NAME="caphe-workflows"
IMAGE_NAME="caphe-workflows"
BACKUP_DIR="backups"

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

################################################################################
# Update Functions
################################################################################

backup_database() {
    print_header "Creating Backup"
    
    cd $PROJECT_DIR/$APP_DIR
    
    # Create backup directory if it doesn't exist
    mkdir -p $BACKUP_DIR
    
    # Create timestamp
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.tar.gz"
    
    print_info "Creating backup: $BACKUP_FILE"
    
    # Backup database and important files
    tar -czf $BACKUP_FILE database/ workflows/ .env 2>/dev/null || true
    
    print_success "Backup created successfully"
    
    # Keep only last 5 backups
    print_info "Cleaning old backups (keeping last 5)..."
    ls -t $BACKUP_DIR/backup_*.tar.gz | tail -n +6 | xargs -r rm
    
    cd - > /dev/null
}

pull_latest_code() {
    print_header "Pulling Latest Code"
    
    cd $PROJECT_DIR
    
    print_info "Fetching latest changes from repository..."
    git fetch origin
    
    # Show what will be updated
    print_info "Changes to be pulled:"
    git log HEAD..origin/master --oneline || git log HEAD..origin/main --oneline
    
    print_info "Pulling changes..."
    git pull
    
    print_success "Code updated successfully"
    
    cd - > /dev/null
}

rebuild_image() {
    print_header "Rebuilding Docker Image"
    
    cd $PROJECT_DIR/$APP_DIR
    
    print_info "Building new Docker image..."
    docker build --no-cache -t $IMAGE_NAME:latest .
    
    print_success "Image rebuilt successfully"
    
    cd - > /dev/null
}

stop_container() {
    print_header "Stopping Current Container"
    
    if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
        print_info "Stopping container..."
        docker stop $CONTAINER_NAME
        print_success "Container stopped"
    else
        print_info "Container is not running"
    fi
}

remove_old_container() {
    print_info "Removing old container..."
    docker rm $CONTAINER_NAME 2>/dev/null || true
    print_success "Old container removed"
}

start_new_container() {
    print_header "Starting Updated Container"
    
    cd $PROJECT_DIR/$APP_DIR
    
    print_info "Starting new container..."
    docker run -d \
        --name $CONTAINER_NAME \
        --restart always \
        -p 8000:8000 \
        -v $(pwd)/database:/app/database \
        -v $(pwd)/workflows:/app/workflows \
        -v $(pwd)/logs:/app/logs \
        --env-file .env \
        $IMAGE_NAME:latest
    
    print_success "Container started successfully"
    
    cd - > /dev/null
}

verify_deployment() {
    print_header "Verifying Deployment"
    
    print_info "Waiting for container to be ready..."
    sleep 5
    
    if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
        print_success "Container is running!"
        echo ""
        docker ps -f name=$CONTAINER_NAME
        echo ""
        print_info "Recent logs:"
        docker logs --tail 20 $CONTAINER_NAME
    else
        print_error "Container failed to start!"
        print_info "Checking logs..."
        docker logs $CONTAINER_NAME
        
        print_error "Update failed. You can restore from backup:"
        echo "  1. Navigate to: cd $PROJECT_DIR/$APP_DIR"
        echo "  2. Find latest backup: ls -lh $BACKUP_DIR/"
        echo "  3. Restore: tar -xzf $BACKUP_DIR/backup_XXXXXXXX_XXXXXX.tar.gz"
        exit 1
    fi
}

cleanup_old_images() {
    print_header "Cleaning Up Old Images"
    
    print_info "Removing unused Docker images..."
    docker image prune -f
    
    print_success "Cleanup completed"
}

display_summary() {
    print_header "Update Complete!"
    
    PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 || echo "your-ec2-ip")
    
    echo ""
    print_success "Caphe Workflows has been updated successfully!"
    echo ""
    echo -e "${GREEN}Application URL:${NC}"
    echo -e "${BLUE}  http://$PUBLIC_IP:8000${NC}"
    echo ""
    echo -e "${YELLOW}Post-Update Checks:${NC}"
    echo "  1. Test the application in your browser"
    echo "  2. Check logs: docker logs -f $CONTAINER_NAME"
    echo "  3. Verify workflows are functioning correctly"
    echo ""
    echo -e "${YELLOW}If there are issues:${NC}"
    echo "  Restore from backup: tar -xzf $PROJECT_DIR/$APP_DIR/$BACKUP_DIR/backup_*.tar.gz"
    echo "  Then rebuild and restart the container"
    echo ""
}

################################################################################
# Main Execution
################################################################################

main() {
    print_header "Caphe Workflows - Update Deployment"
    
    # Check if project directory exists
    if [ ! -d "$PROJECT_DIR" ]; then
        print_error "Project directory not found: $PROJECT_DIR"
        print_info "Have you run the initial deployment script?"
        exit 1
    fi
    
    echo "This script will:"
    echo "  1. Create a backup of your current deployment"
    echo "  2. Pull the latest code from the repository"
    echo "  3. Rebuild the Docker image"
    echo "  4. Stop the current container"
    echo "  5. Start a new container with the updated code"
    echo "  6. Verify the deployment"
    echo ""
    
    read -p "Do you want to continue? (y/n) " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Update cancelled"
        exit 0
    fi
    
    # Execute update steps
    backup_database
    pull_latest_code
    rebuild_image
    stop_container
    remove_old_container
    start_new_container
    verify_deployment
    cleanup_old_images
    
    display_summary
}

# Run main function
main "$@"
