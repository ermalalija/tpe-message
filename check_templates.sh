#!/bin/bash
# Check if templates are copied into Docker container

echo "🔍 Checking Templates in Docker Container"
echo "========================================="

echo "📁 Local templates directory:"
ls -la templates/

echo ""
echo "🐳 Checking templates in container:"
docker-compose exec gmail-whatsapp-bridge ls -la templates/ 2>/dev/null || echo "❌ templates/ directory not found in container"

echo ""
echo "📄 Checking specific template files:"
docker-compose exec gmail-whatsapp-bridge ls -la templates/login.html 2>/dev/null || echo "❌ login.html not found"
docker-compose exec gmail-whatsapp-bridge ls -la templates/settings.html 2>/dev/null || echo "❌ settings.html not found"

echo ""
echo "🔧 Quick Fix Commands:"
echo "====================="
echo "# Rebuild container to ensure templates are copied:"
echo "docker-compose down"
echo "docker-compose build --no-cache"
echo "docker-compose up -d"
echo ""
echo "# Or manually copy templates:"
echo "docker cp templates/ gmail-whatsapp-bridge:/app/templates/"
echo ""
echo "# Check again:"
echo "docker-compose exec gmail-whatsapp-bridge ls -la templates/"

echo ""
echo "🎯 Expected Result:"
echo "=================="
echo "You should see:"
echo "- templates/login.html"
echo "- templates/settings.html"
echo "in the container's /app/templates/ directory" 