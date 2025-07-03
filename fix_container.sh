#!/bin/bash
# Fix Container Health Check Issue

echo "🔧 Fixing Gmail-to-WhatsApp Bridge Container"
echo "============================================"

# Stop and remove existing container
echo "Stopping existing container..."
docker-compose down

# Rebuild the container with new health check
echo "Rebuilding container with fixed health check..."
docker-compose build --no-cache

# Start the container
echo "Starting container..."
docker-compose up -d

# Wait a moment for container to start
echo "Waiting for container to start..."
sleep 10

# Check container status
echo "Checking container status..."
docker-compose ps

# Check logs
echo "Checking container logs..."
docker-compose logs --tail=20

# Test health endpoint
echo "Testing health endpoint..."
docker-compose exec gmail-whatsapp-bridge curl -f http://localhost:5000/health || echo "Health check failed"

echo ""
echo "🎯 Next Steps:"
echo "=============="
echo "1. Check if container is now 'healthy': docker-compose ps"
echo "2. Access your app: http://your-ec2-ip:5000"
echo "3. Login with: ErmalAlija / Prishtina1997!"
echo "4. If still unhealthy, check logs: docker-compose logs -f" 