#!/bin/bash

# Flask Application Deployment Script
# This script builds and deploys the Flask application with security best practices

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="flask-app"
TAG="latest"
CONTAINER_NAME="flask-app-container"
PORT="5851"

echo -e "${GREEN}🚀 Starting Flask Application Deployment${NC}"

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

print_status "Docker is running"

# Stop and remove existing container if it exists
if docker ps -a --format "table {{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
    print_warning "Stopping existing container..."
    docker stop ${CONTAINER_NAME} || true
    docker rm ${CONTAINER_NAME} || true
    print_status "Existing container removed"
fi

# Remove existing image if it exists
if docker images --format "table {{.Repository}}:{{.Tag}}" | grep -q "^${IMAGE_NAME}:${TAG}$"; then
    print_warning "Removing existing image..."
    docker rmi ${IMAGE_NAME}:${TAG} || true
    print_status "Existing image removed"
fi

# Build the Docker image
print_status "Building Docker image..."
docker build --target production -t ${IMAGE_NAME}:${TAG} .

if [ $? -eq 0 ]; then
    print_status "Docker image built successfully"
else
    print_error "Failed to build Docker image"
    exit 1
fi

# Run security scan (if available)
if command -v docker scout &> /dev/null; then
    print_status "Running security scan..."
    docker scout cves ${IMAGE_NAME}:${TAG} || print_warning "Security scan failed or vulnerabilities found"
else
    print_warning "Docker Scout not available. Consider installing for security scanning."
fi

# Run the container
print_status "Starting container..."
docker run -d \
    --name ${CONTAINER_NAME} \
    -p ${PORT}:${PORT} \
    -e FLASK_ENV=production \
    -e FLASK_APP=app.py \
    --restart unless-stopped \
    --security-opt no-new-privileges \
    --read-only \
    --tmpfs /tmp \
    --tmpfs /var/tmp \
    ${IMAGE_NAME}:${TAG}

if [ $? -eq 0 ]; then
    print_status "Container started successfully"
else
    print_error "Failed to start container"
    exit 1
fi

# Wait for application to start
print_status "Waiting for application to start..."
sleep 5

# Check if application is responding
if curl -f http://localhost:${PORT}/health > /dev/null 2>&1; then
    print_status "Application is healthy and responding"
else
    print_warning "Health check failed. Checking container logs..."
    docker logs ${CONTAINER_NAME}
    print_error "Application may not be running properly"
    exit 1
fi

# Display container information
echo -e "\n${GREEN}📊 Deployment Summary:${NC}"
echo "Container Name: ${CONTAINER_NAME}"
echo "Image: ${IMAGE_NAME}:${TAG}"
echo "Port: ${PORT}"
echo "Health Check: http://localhost:${PORT}/health"
echo "Application: http://localhost:${PORT}/"

# Display container status
echo -e "\n${GREEN}📋 Container Status:${NC}"
docker ps --filter "name=${CONTAINER_NAME}" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

print_status "Deployment completed successfully! 🎉"

echo -e "\n${YELLOW}Useful commands:${NC}"
echo "View logs: docker logs -f ${CONTAINER_NAME}"
echo "Stop container: docker stop ${CONTAINER_NAME}"
echo "Remove container: docker rm ${CONTAINER_NAME}"
echo "Health check: curl http://localhost:${PORT}/health" 