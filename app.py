import os
import sqlite3
import json
import base64
from datetime import datetime
from functools import wraps
from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator
import threading
import time

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Configuration
UPLOAD_FOLDER = 'credentials'
ALLOWED_EXTENSIONS = {'json'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# Hardcoded credentials
ADMIN_USERNAME = 'ErmalAlija'
ADMIN_PASSWORD = 'Prishtina1997!'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    conn = sqlite3.connect('config.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create settings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    # Create filters table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS filters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT UNIQUE
        )
    ''')
    
    # Create conversation_map table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversation_map (
            thread_id TEXT PRIMARY KEY,
            whatsapp_user_number TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_setting(key, default=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
    result = cursor.fetchone()
    conn.close()
    return result['value'] if result else default

def set_setting(key, value):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, value))
    conn.commit()
    conn.close()

def get_filters():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT keyword FROM filters ORDER BY keyword')
    filters = [row['keyword'] for row in cursor.fetchall()]
    conn.close()
    return filters

def set_filters(keywords):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM filters')
    for keyword in keywords:
        if keyword.strip():
            cursor.execute('INSERT INTO filters (keyword) VALUES (?)', (keyword.strip(),))
    conn.commit()
    conn.close()

def store_conversation_mapping(thread_id, whatsapp_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO conversation_map (thread_id, whatsapp_user_number, last_updated)
        VALUES (?, ?, CURRENT_TIMESTAMP)
    ''', (thread_id, whatsapp_number))
    conn.commit()
    conn.close()

def get_thread_id_for_whatsapp(whatsapp_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT thread_id FROM conversation_map 
        WHERE whatsapp_user_number = ? 
        ORDER BY last_updated DESC 
        LIMIT 1
    ''', (whatsapp_number,))
    result = cursor.fetchone()
    conn.close()
    return result['thread_id'] if result else None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'authenticated' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('settings'))
        else:
            flash('Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))

@app.route('/health')
def health():
    """Health check endpoint for Docker"""
    return {'status': 'healthy', 'message': 'Gmail-to-WhatsApp Bridge is running'}, 200

@app.route('/')
@login_required
def index():
    return redirect(url_for('settings'))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        # Handle file upload for Gmail credentials
        if 'gmail_credentials' in request.files:
            file = request.files['gmail_credentials']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                set_setting('gmail_credentials_path', filepath)
                flash('Gmail credentials uploaded successfully')
        
        # Handle other settings
        twilio_sid = request.form.get('twilio_sid')
        twilio_token = request.form.get('twilio_token')
        twilio_whatsapp_number = request.form.get('twilio_whatsapp_number')
        target_whatsapp_number = request.form.get('target_whatsapp_number')
        filter_keywords = request.form.get('filter_keywords', '').split('\n')
        
        if twilio_sid:
            set_setting('twilio_sid', twilio_sid)
        if twilio_token:
            set_setting('twilio_token', twilio_token)
        if twilio_whatsapp_number:
            set_setting('twilio_whatsapp_number', twilio_whatsapp_number)
        if target_whatsapp_number:
            set_setting('target_whatsapp_number', target_whatsapp_number)
        
        set_filters(filter_keywords)
        
        flash('Settings updated successfully')
        return redirect(url_for('settings'))
    
    # Get current settings
    current_settings = {
        'twilio_sid': get_setting('twilio_sid', ''),
        'twilio_token': get_setting('twilio_token', ''),
        'twilio_whatsapp_number': get_setting('twilio_whatsapp_number', ''),
        'target_whatsapp_number': get_setting('target_whatsapp_number', ''),
        'filter_keywords': '\n'.join(get_filters())
    }
    
    return render_template('settings.html', settings=current_settings)

@app.route('/twilio-webhook', methods=['POST'])
def twilio_webhook():
    # Validate Twilio request
    twilio_sid = get_setting('twilio_sid')
    twilio_token = get_setting('twilio_token')
    
    if not twilio_sid or not twilio_token:
        return 'Configuration error', 500
    
    validator = RequestValidator(twilio_token)
    url = request.url
    signature = request.headers.get('X-Twilio-Signature', '')
    params = request.form.to_dict()
    
    if not validator.validate(url, params, signature):
        return 'Invalid signature', 403
    
    # Process incoming message
    from_number = request.form.get('From', '')
    message_body = request.form.get('Body', '')
    
    if from_number and message_body:
        # Remove 'whatsapp:' prefix if present
        whatsapp_number = from_number.replace('whatsapp:', '')
        
        # Get the thread ID for this WhatsApp number
        thread_id = get_thread_id_for_whatsapp(whatsapp_number)
        
        if thread_id:
            # Send reply to Gmail
            try:
                send_gmail_reply(thread_id, message_body)
                response = MessagingResponse()
                response.message("Message sent to Gmail successfully!")
                return str(response)
            except Exception as e:
                print(f"Error sending Gmail reply: {e}")
                response = MessagingResponse()
                response.message("Sorry, there was an error sending your message to Gmail.")
                return str(response)
        else:
            response = MessagingResponse()
            response.message("No active conversation found. Please wait for an email to be forwarded to you first.")
            return str(response)
    
    return 'OK'

def send_gmail_reply(thread_id, message_body):
    """Send a reply to a Gmail thread"""
    try:
        credentials_path = get_setting('gmail_credentials_path')
        if not credentials_path or not os.path.exists(credentials_path):
            raise Exception("Gmail credentials not found")
        
        # Load credentials and build service
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
        creds = flow.run_local_server(port=0)
        
        service = build('gmail', 'v1', credentials=creds)
        
        # Create the message
        message = {
            'threadId': thread_id,
            'raw': base64.urlsafe_b64encode(
                f'Content-Type: text/plain; charset="UTF-8"\n'
                f'MIME-Version: 1.0\n'
                f'Content-Transfer-Encoding: 7bit\n'
                f'In-Reply-To: <{thread_id}@gmail.com>\n'
                f'References: <{thread_id}@gmail.com>\n'
                f'Subject: Re: WhatsApp Reply\n\n'
                f'{message_body}'.encode('utf-8')
            ).decode('utf-8')
        }
        
        # Send the message
        service.users().messages().send(userId='me', body=message).execute()
        
    except Exception as e:
        print(f"Error in send_gmail_reply: {e}")
        raise

if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='0.0.0.0', port=5000) 