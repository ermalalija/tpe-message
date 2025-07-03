#!/bin/bash
# Network Troubleshooting Script for EC2 Flask App

echo "🔍 EC2 Network Troubleshooting Script"
echo "====================================="

# Get instance info
echo "📋 Instance Information:"
echo "Public IP: $(curl -s ifconfig.me)"
echo "Private IP: $(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)"
echo "Instance ID: $(curl -s http://169.254.169.254/latest/meta-data/instance-id)"

echo ""
echo "🔧 Checking Flask Application:"
echo "=============================="

# Check if Flask is running
if pgrep -f "python.*app.py" > /dev/null; then
    echo "✅ Flask app is running"
    ps aux | grep "python.*app.py" | grep -v grep
else
    echo "❌ Flask app is NOT running"
fi

echo ""
echo "🌐 Checking Network Ports:"
echo "=========================="

# Check if port 5000 is listening
if netstat -tlnp 2>/dev/null | grep ":5000" > /dev/null; then
    echo "✅ Port 5000 is listening"
    netstat -tlnp | grep ":5000"
else
    echo "❌ Port 5000 is NOT listening"
fi

echo ""
echo "🔥 Checking Firewall Status:"
echo "============================"

# Check UFW status
if command -v ufw >/dev/null 2>&1; then
    echo "UFW Status:"
    sudo ufw status
    echo ""
    echo "To allow port 5000, run: sudo ufw allow 5000"
else
    echo "UFW not installed"
fi

echo ""
echo "🔒 Security Group Check:"
echo "======================="
echo "⚠️  IMPORTANT: Check your AWS Security Group!"
echo "1. Go to AWS Console → EC2 → Security Groups"
echo "2. Select your instance's security group"
echo "3. Click 'Inbound rules' → 'Edit inbound rules'"
echo "4. Add rule:"
echo "   - Type: Custom TCP"
echo "   - Protocol: TCP"
echo "   - Port: 5000"
echo "   - Source: 0.0.0.0/0"
echo "   - Description: Flask App"

echo ""
echo "🧪 Testing Connectivity:"
echo "======================="

# Test local connectivity
echo "Testing localhost:5000..."
if curl -s http://localhost:5000 > /dev/null 2>&1; then
    echo "✅ Local access works"
else
    echo "❌ Local access fails"
fi

# Test public IP connectivity
PUBLIC_IP=$(curl -s ifconfig.me)
echo "Testing $PUBLIC_IP:5000..."
if curl -s --connect-timeout 5 http://$PUBLIC_IP:5000 > /dev/null 2>&1; then
    echo "✅ Public IP access works"
else
    echo "❌ Public IP access fails (likely security group issue)"
fi

echo ""
echo "📝 Quick Fix Commands:"
echo "====================="
echo "# Allow port 5000 in firewall:"
echo "sudo ufw allow 5000"
echo ""
echo "# Start Flask app:"
echo "python app.py"
echo ""
echo "# Test with simple server:"
echo "python test_server.py"
echo ""
echo "# Check if port is open:"
echo "sudo netstat -tlnp | grep 5000"

echo ""
echo "🎯 Next Steps:"
echo "=============="
echo "1. Fix security group rules in AWS Console"
echo "2. Allow port 5000 in UFW: sudo ufw allow 5000"
echo "3. Restart Flask app: python app.py"
echo "4. Test again: http://$PUBLIC_IP:5000" 