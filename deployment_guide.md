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
sudo apt install docker.io docker-compose -y
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
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs
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

## 🌐 Domain Setup for EC2 Instance

### Step 1: Register a Domain Name

#### Option A: AWS Route 53 (Recommended)
1. **Go to Route 53 Console**:
   - AWS Console → Route 53 → Registered domains
   - Click "Register Domain"

2. **Search for Domain**:
   - Enter your desired domain name
   - Choose from available options
   - Select domain extension (.com, .net, etc.)

3. **Complete Registration**:
   - Fill in contact information
   - Choose registration period (1-10 years)
   - Complete payment

#### Option B: External Domain Registrar
- **Popular Options**: GoDaddy, Namecheap, Google Domains
- Register your domain and note the nameservers
- You'll configure DNS records in the next step

### Step 2: Configure DNS Records

#### For AWS Route 53:
1. **Create Hosted Zone**:
   - Route 53 → Hosted zones
   - Click "Create hosted zone"
   - Enter your domain name
   - Click "Create"

2. **Create A Record**:
   - Click on your hosted zone
   - Click "Create record"
   - **Record type**: A
   - **Record name**: Leave blank (for root domain) or enter subdomain
   - **Value**: Your EC2 instance's **Elastic IP** (recommended) or public IP
   - **TTL**: 300 seconds
   - Click "Create records"

3. **Create CNAME Record (Optional for www)**:
   - Click "Create record"
   - **Record type**: CNAME
   - **Record name**: www
   - **Value**: your-domain.com
   - **TTL**: 300 seconds
   - Click "Create records"

#### For External Domain Registrars:
1. **Get Nameservers from Route 53**:
   - Create hosted zone in Route 53
   - Note the 4 nameservers provided

2. **Update Nameservers**:
   - Go to your domain registrar's DNS settings
   - Replace existing nameservers with Route 53 nameservers
   - Save changes

3. **Create A Record in Route 53**:
   - Follow steps above for creating A record

### Step 3: Set Up Elastic IP (Recommended)

1. **Allocate Elastic IP**:
   - EC2 Console → Elastic IPs
   - Click "Allocate Elastic IP address"
   - Click "Allocate"

2. **Associate with Instance**:
   - Select your Elastic IP
   - Click "Actions" → "Associate Elastic IP address"
   - Select your EC2 instance
   - Click "Associate"

3. **Update DNS Record**:
   - Go back to Route 53
   - Update your A record with the Elastic IP address

### Step 4: Configure Nginx

1. **Update Nginx Configuration**:
```bash
sudo nano /etc/nginx/sites-available/gmail-whatsapp-bridge
```

Replace `your-domain.com` with your actual domain:
```nginx
server {
    listen 80;
    server_name your-actual-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

2. **Test and Reload Nginx**:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

### Step 5: Install SSL Certificate

1. **Install Certbot**:
```bash
sudo apt install certbot python3-certbot-nginx -y
```

2. **Obtain SSL Certificate**:
```bash
sudo certbot --nginx -d your-actual-domain.com
```

3. **Test Auto-Renewal**:
```bash
sudo certbot renew --dry-run
```

### Step 6: Update Twilio Webhook

1. **Get Your Webhook URL**:
   - Your webhook URL will be: `https://your-actual-domain.com/twilio-webhook`

2. **Update Twilio Console**:
   - Go to Twilio Console → Messaging → Settings → WhatsApp Sandbox
   - Set webhook URL to your new HTTPS URL
   - Method: POST
   - Save changes

### Step 7: Test Your Setup

1. **Test Domain Resolution**:
```bash
# From your local machine
nslookup your-actual-domain.com
ping your-actual-domain.com
```

2. **Test HTTPS Access**:
   - Open browser: `https://your-actual-domain.com`
   - Should redirect to HTTPS automatically
   - Verify SSL certificate is valid

3. **Test Twilio Webhook**:
   - Send a WhatsApp message to your Twilio number
   - Check if webhook receives the message
   - Verify in your application logs

### DNS Propagation Time

- **Initial Setup**: 5-30 minutes
- **Full Propagation**: Up to 48 hours
- **Testing**: Use `dig` or `nslookup` to check propagation

### Troubleshooting Domain Issues

1. **Domain Not Resolving**:
   - Check DNS records are correct
   - Verify nameservers are updated
   - Wait for propagation (up to 48 hours)

2. **SSL Certificate Issues**:
   - Ensure domain resolves to your server
   - Check firewall allows port 80/443
   - Verify Nginx configuration

3. **Twilio Webhook Fails**:
   - Ensure HTTPS URL is accessible
   - Check SSL certificate is valid
   - Verify webhook endpoint responds correctly

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