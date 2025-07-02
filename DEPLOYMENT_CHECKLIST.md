# Deployment Checklist

## ✅ Prerequisites

- [ ] Python 3.8+ installed (or Docker Desktop)
- [ ] Google Cloud Console account
- [ ] Twilio account with WhatsApp capabilities
- [ ] Public HTTPS URL (for production)

## 🚀 Deployment Method

Choose your deployment method:

### Option A: Windows with Python
- [ ] Run `deploy_windows.bat` or `deploy_windows.ps1`
- [ ] Or manually install dependencies: `pip install -r requirements.txt`
- [ ] Start web server: `python app.py`
- [ ] Start worker: `python worker.py`

### Option B: Docker
- [ ] Install Docker Desktop
- [ ] Build image: `docker build -t gmail-whatsapp-bridge .`
- [ ] Run: `docker-compose up -d`

### Option C: AWS EC2
- [ ] Launch Ubuntu Server 22.04 LTS EC2 instance
- [ ] Install Docker on EC2
- [ ] Deploy application
- [ ] Configure domain and SSL

## 🔧 Google Cloud Setup

- [ ] Create Google Cloud project
- [ ] Enable Gmail API
- [ ] Create OAuth 2.0 credentials
- [ ] Download `credentials.json`
- [ ] Configure OAuth consent screen
- [ ] Add your email as test user

## 📱 Twilio Setup

- [ ] Create Twilio account
- [ ] Verify phone number
- [ ] Enable WhatsApp sandbox
- [ ] Get Account SID and Auth Token
- [ ] Note your Twilio WhatsApp number

## ⚙️ Application Configuration

- [ ] Access web interface (http://localhost:5000)
- [ ] Login with: ErmalAlija / Prishtina1997!
- [ ] Upload `credentials.json` file
- [ ] Enter Twilio Account SID
- [ ] Enter Twilio Auth Token
- [ ] Enter Twilio WhatsApp number
- [ ] Enter target WhatsApp number
- [ ] Configure email filter keywords
- [ ] Copy webhook URL from interface

## 🔗 Webhook Configuration

- [ ] Go to Twilio Console
- [ ] Navigate to Messaging → Settings → WhatsApp Sandbox
- [ ] Set webhook URL: `https://your-domain.com/twilio-webhook`
- [ ] Set HTTP method to POST

## 🧪 Testing

- [ ] Send test email with filter keyword
- [ ] Verify email forwarded to WhatsApp
- [ ] Reply to WhatsApp message
- [ ] Verify reply appears in Gmail thread
- [ ] Check application logs for errors

## 🔒 Security (Production)

- [ ] Change default admin credentials
- [ ] Use HTTPS in production
- [ ] Secure file permissions
- [ ] Set up monitoring and logging
- [ ] Configure backups

## 📊 Monitoring

- [ ] Check application logs regularly
- [ ] Monitor Gmail API quotas
- [ ] Monitor Twilio usage and costs
- [ ] Set up alerts for errors

## 🆘 Troubleshooting

If you encounter issues:

1. **Check logs**:
   ```bash
   # Docker
   docker-compose logs -f
   
   # Python
   Check console output
   ```

2. **Common issues**:
   - Gmail authentication errors → Check credentials.json
   - Twilio webhook issues → Verify HTTPS URL
   - Email not forwarding → Check filter keywords
   - Database errors → Check file permissions

3. **Get help**:
   - Review deployment_guide.md
   - Check README.md
   - Create issue in repository

## 📞 Support Information

- **Application URL**: [Your deployed URL]
- **Admin Login**: ErmalAlija / Prishtina1997!
- **Webhook URL**: [Your webhook URL]
- **Twilio WhatsApp Number**: [Your Twilio number]
- **Target WhatsApp Number**: [Your target number]

## 📝 Notes

- Keep your credentials secure
- Monitor your Twilio usage to avoid unexpected charges
- Regular backups of config.db are recommended
- Update dependencies regularly for security

---

**Deployment completed on**: _______________
**Deployed by**: _______________
**Environment**: Development/Production 