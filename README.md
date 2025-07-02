# Gmail-to-WhatsApp Bridge

A robust, 24/7 Python application that acts as a bridge between Gmail and WhatsApp using the Twilio API. The application consists of a background worker that processes emails and a Flask web application for configuration and reply handling.

## Features

- **Email Polling**: Checks Gmail every 60 seconds for new unread emails
- **Smart Filtering**: Forwards emails based on configurable keywords in the subject line
- **WhatsApp Integration**: Sends filtered emails to WhatsApp via Twilio
- **Reply Handling**: Processes WhatsApp replies and sends them back to the original Gmail thread
- **Web Configuration**: Password-protected web interface for managing settings
- **Docker Support**: Complete containerization for easy deployment
- **Database Storage**: SQLite database for conversation mapping and settings

## Architecture

### Core Components

1. **Background Worker** (`worker.py`): Continuously polls Gmail for new emails
2. **Web Application** (`app.py`): Flask app handling webhooks and configuration
3. **Database** (`config.db`): SQLite database storing settings and conversation mappings
4. **Web Interface**: Modern, responsive UI for configuration management

### Database Schema

- **settings**: Key-value store for configuration
- **filters**: Email filter keywords
- **conversation_map**: Maps Gmail thread IDs to WhatsApp numbers

## Prerequisites

Before setting up the application, you'll need:

1. **Google Cloud Console Account**
2. **Twilio Account** with WhatsApp capabilities
3. **Docker** (for containerized deployment)
4. **Public HTTPS URL** (for Twilio webhooks)

## Setup Instructions

### Step 1: Google Cloud Console Setup

1. **Create a Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one

2. **Enable Gmail API**:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Gmail API" and enable it

3. **Create OAuth 2.0 Credentials**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Choose "Desktop application" as the application type
   - Download the credentials file as `credentials.json`

4. **Configure OAuth Consent Screen**:
   - Go to "APIs & Services" > "OAuth consent screen"
   - Choose "External" user type
   - Add your email as a test user
   - Add the following scopes:
     - `https://www.googleapis.com/auth/gmail.modify`

### Step 2: Twilio Setup

1. **Create Twilio Account**:
   - Sign up at [Twilio](https://www.twilio.com/)
   - Verify your phone number

2. **Enable WhatsApp Sandbox**:
   - Go to Twilio Console > Messaging > Try it out > Send a WhatsApp message
   - Follow the instructions to join the WhatsApp sandbox
   - Note your Twilio WhatsApp number

3. **Get Account Credentials**:
   - In Twilio Console, find your Account SID and Auth Token
   - Keep these secure - you'll need them for configuration

### Step 3: Application Setup

1. **Clone or Download the Application**:
   ```bash
   git clone <repository-url>
   cd gmail-whatsapp-bridge
   ```

2. **Build and Run with Docker**:
   ```bash
   # Build the Docker image
   docker build -t gmail-whatsapp-bridge .
   
   # Run the container
   docker run -d \
     --name gmail-whatsapp-bridge \
     -p 5000:5000 \
     -v $(pwd)/credentials:/app/credentials \
     -v $(pwd)/config.db:/app/config.db \
     gmail-whatsapp-bridge
   ```

3. **Access the Web Interface**:
   - Open your browser and go to `http://localhost:5000`
   - Login with:
     - Username: `ErmalAlija`
     - Password: `Prishtina1997!`

### Step 4: Configuration

1. **Upload Gmail Credentials**:
   - In the web interface, upload your `credentials.json` file
   - The application will guide you through the OAuth flow

2. **Configure Twilio Settings**:
   - Enter your Twilio Account SID
   - Enter your Twilio Auth Token
   - Enter your Twilio WhatsApp number
   - Enter the target WhatsApp number (where emails will be forwarded)

3. **Set Email Filters**:
   - Add keywords or phrases that should trigger email forwarding
   - One keyword per line
   - Case-insensitive matching

4. **Configure Webhook**:
   - Copy the webhook URL shown in the interface
   - In Twilio Console, go to Messaging > Settings > WhatsApp Sandbox Settings
   - Set the webhook URL to: `https://your-domain.com/twilio-webhook`
   - Set HTTP method to POST

### Step 5: Testing

1. **Test Email Forwarding**:
   - Send an email to your Gmail account with a subject containing one of your filter keywords
   - Check if the email is forwarded to WhatsApp

2. **Test Reply Handling**:
   - Reply to a forwarded WhatsApp message
   - Check if the reply appears in the original Gmail thread

## Production Deployment

### AWS Deployment

1. **EC2 Instance Setup**:
   ```bash
   # Launch an EC2 instance with Ubuntu
   # Install Docker
   sudo apt update
   sudo apt install docker.io
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -aG docker ubuntu
   ```

2. **Application Deployment**:
   ```bash
   # Clone the application
   git clone <repository-url>
   cd gmail-whatsapp-bridge
   
   # Build and run
   docker build -t gmail-whatsapp-bridge .
   docker run -d \
     --name gmail-whatsapp-bridge \
     --restart unless-stopped \
     -p 80:5000 \
     -v $(pwd)/credentials:/app/credentials \
     -v $(pwd)/config.db:/app/config.db \
     gmail-whatsapp-bridge
   ```

3. **Domain and SSL**:
   - Set up a domain name pointing to your EC2 instance
   - Configure SSL certificate (Let's Encrypt recommended)
   - Update Twilio webhook URL to use HTTPS

### Environment Variables

For production, consider using environment variables for sensitive data:
```bash
export FLASK_SECRET_KEY="your-secure-secret-key"
export ADMIN_USERNAME="your-admin-username"
export ADMIN_PASSWORD="your-secure-password"
```

## Security Considerations

1. **Change Default Credentials**: Update the hardcoded admin credentials in production
2. **Use HTTPS**: Always use HTTPS in production for webhook endpoints
3. **Secure File Permissions**: Ensure credentials files are properly secured
4. **Regular Updates**: Keep dependencies updated
5. **Monitor Logs**: Regularly check application logs for issues

## Troubleshooting

### Common Issues

1. **Gmail Authentication Errors**:
   - Ensure `credentials.json` is properly uploaded
   - Check that OAuth consent screen is configured correctly
   - Verify the Gmail API is enabled

2. **Twilio Webhook Issues**:
   - Ensure webhook URL is accessible from the internet
   - Verify HTTPS is used in production
   - Check Twilio logs for webhook delivery status

3. **Email Not Forwarding**:
   - Check if filter keywords are configured
   - Verify target WhatsApp number is correct
   - Check application logs for errors

4. **Database Issues**:
   - Ensure the application has write permissions to the database file
   - Check if the database file is properly mounted in Docker

### Logs

View application logs:
```bash
# Docker logs
docker logs gmail-whatsapp-bridge

# Follow logs in real-time
docker logs -f gmail-whatsapp-bridge
```

## API Endpoints

- `GET /` - Redirects to settings page
- `GET /login` - Login page
- `POST /login` - Login form submission
- `GET /settings` - Configuration page
- `POST /settings` - Save configuration
- `POST /twilio-webhook` - Twilio webhook endpoint

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review application logs
3. Create an issue in the repository

## Changelog

### Version 1.0.0
- Initial release
- Gmail polling and filtering
- WhatsApp integration via Twilio
- Web configuration interface
- Docker support
- Reply handling functionality 