# Gmail-to-WhatsApp Bridge Deployment Guide

## 🚀 Quick Start Options

### Option 1: Windows with Python (Development)

#### Step 1: Install Python
1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, **check "Add Python to PATH"**
3. Verify installation:
   ```cmd
   python --version
   pip --version
   ```

#### Step 2: Install Dependencies
```cmd
pip install -r requirements.txt
```

#### Step 3: Run the Application
```cmd
# Terminal 1: Start the web server
python app.py

# Terminal 2: Start the background worker
python worker.py
```

#### Step 4: Access the Application
- Open browser: `http://localhost:5000`
- Login: `ErmalAlija` / `Prishtina1997!`

### Option 2: Docker Deployment (Recommended for Production)

#### Step 1: Install Docker Desktop
1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Install and restart your computer
3. Verify installation:
   ```cmd
   docker --version
   docker-compose --version
   ```

#### Step 2: Build and Run
```cmd
# Build the Docker image
docker build -t gmail-whatsapp-bridge .

# Run with Docker Compose
docker-compose up -d
```

#### Step 3: Access the Application
- Open browser: `http://localhost:5000`
- Login: `ErmalAlija` / `Prishtina1997!`

### Option 3: AWS EC2 Deployment (Production)

#### Step 1: Launch EC2 Instance
1. Go to AWS Console → EC2
2. Launch Instance:
   - **AMI**: Ubuntu Server 22.04 LTS (ssd volume type)
   - **Instance Type**: t2.micro (free tier) or t2.small
   - **Security Group**: Allow ports 22 (SSH), 80 (HTTP), 443 (HTTPS)
   - **Key Pair**: Create or select existing

#### Step 2: Connect and Setup
```bash
# SSH into your instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker (Ubuntu 22.04 method)
sudo apt install docker.io docker-compose-plugin -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu

# Logout and login again
exit
ssh -i your-key.pem ubuntu@your-ec2-ip
```

#### Step 3: Deploy Application
```bash
# Clone your application (or upload files)
git clone <your-repo-url>
cd gmail-whatsapp-bridge

# Build and run
docker compose up -d

# Check status
docker compose ps
docker compose logs
```

#### Step 4: Configure Domain and SSL
```bash
# Install Nginx
sudo apt install nginx -y

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/gmail-whatsapp-bridge
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/gmail-whatsapp-bridge /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Install SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### Option 4: Heroku Deployment

#### Step 1: Install Heroku CLI
1. Download from [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)
2. Install and login:
   ```cmd
   heroku login
   ```

#### Step 2: Create Heroku App
```cmd
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit"

# Create Heroku app
heroku create your-app-name

# Add buildpacks
heroku buildpacks:add heroku/python

# Deploy
git push heroku main
```

#### Step 3: Configure Environment Variables
```cmd
heroku config:set FLASK_ENV=production
heroku config:set ADMIN_USERNAME=ErmalAlija
heroku config:set ADMIN_PASSWORD=Prishtina1997!
```

## 🔧 Configuration Steps

### Step 1: Google Cloud Console Setup

1. **Create Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create new project or select existing

2. **Enable Gmail API**:
   - APIs & Services → Library
   - Search "Gmail API" → Enable

3. **Create Credentials**:
   - APIs & Services → Credentials
   - Create Credentials → OAuth 2.0 Client IDs
   - Application type: Desktop application
   - Download as `credentials.json`

4. **Configure OAuth Consent**:
   - APIs & Services → OAuth consent screen
   - User type: External
   - Add your email as test user
   - Add scope: `https://www.googleapis.com/auth/gmail.modify`

### Step 2: Twilio Setup

1. **Create Account**:
   - Sign up at [twilio.com](https://www.twilio.com/)
   - Verify your phone number

2. **Enable WhatsApp**:
   - Console → Messaging → Try it out → Send WhatsApp message
   - Follow sandbox instructions
   - Note your Twilio WhatsApp number

3. **Get Credentials**:
   - Console → Account Info
   - Copy Account SID and Auth Token

### Step 3: Application Configuration

1. **Access Web Interface**:
   - Navigate to your deployed URL
   - Login: `ErmalAlija` / `Prishtina1997!`

2. **Upload Gmail Credentials**:
   - Upload `credentials.json` file
   - Complete OAuth flow

3. **Configure Twilio**:
   - Enter Account SID
   - Enter Auth Token
   - Enter Twilio WhatsApp number
   - Enter target WhatsApp number

4. **Set Email Filters**:
   - Add keywords (one per line)
   - Example: URGENT, CRITICAL, ALERT

5. **Configure Webhook**:
   - Copy webhook URL from interface
   - Twilio Console → Messaging → Settings → WhatsApp Sandbox
   - Set webhook URL: `https://your-domain.com/twilio-webhook`
   - Method: POST

## 🧪 Testing

### Test Email Forwarding
1. Send email to your Gmail with subject containing filter keyword
2. Check if forwarded to WhatsApp

### Test Reply Handling
1. Reply to forwarded WhatsApp message
2. Check if reply appears in Gmail thread

### Check Logs
```bash
# Docker logs
docker-compose logs -f

# Heroku logs
heroku logs --tail

# EC2 logs
docker-compose logs -f gmail-whatsapp-bridge
```

## 🔒 Security Checklist

- [ ] Change default admin credentials in production
- [ ] Use HTTPS in production
- [ ] Secure file permissions
- [ ] Regular dependency updates
- [ ] Monitor application logs
- [ ] Backup database regularly

## 🚨 Troubleshooting

### Common Issues

1. **Gmail Authentication Errors**:
   - Verify `credentials.json` is uploaded
   - Check OAuth consent screen configuration
   - Ensure Gmail API is enabled

2. **Twilio Webhook Issues**:
   - Verify webhook URL is accessible
   - Use HTTPS in production
   - Check Twilio logs

3. **Email Not Forwarding**:
   - Check filter keywords configuration
   - Verify target WhatsApp number
   - Review application logs

4. **Docker Issues**:
   - Ensure Docker is running
   - Check port conflicts
   - Verify volume mounts

### Getting Help

1. Check application logs
2. Review this deployment guide
3. Check the main README.md
4. Create an issue in the repository

## 📞 Support

For deployment issues:
1. Check logs first
2. Verify all prerequisites are met
3. Test with local deployment first
4. Ensure all configuration steps are completed 