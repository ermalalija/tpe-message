import os
import sqlite3
import time
import base64
import email
from datetime import datetime
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from twilio.rest import Client
import re

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_db_connection():
    conn = sqlite3.connect('config.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_setting(key, default=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
    result = cursor.fetchone()
    conn.close()
    return result['value'] if result else default

def get_filters():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT keyword FROM filters ORDER BY keyword')
    filters = [row['keyword'] for row in cursor.fetchall()]
    conn.close()
    return filters

def store_conversation_mapping(thread_id, whatsapp_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO conversation_map (thread_id, whatsapp_user_number, last_updated)
        VALUES (?, ?, CURRENT_TIMESTAMP)
    ''', (thread_id, whatsapp_number))
    conn.commit()
    conn.close()

def get_gmail_service():
    """Get authenticated Gmail service"""
    credentials_path = get_setting('gmail_credentials_path')
    if not credentials_path or not os.path.exists(credentials_path):
        raise Exception("Gmail credentials not found")
    
    # Load credentials and build service
    flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
    creds = flow.run_local_server(port=0)
    
    return build('gmail', 'v1', credentials=creds)

def extract_email_body(message_data):
    """Extract plain text body from email message"""
    try:
        if 'parts' in message_data['payload']:
            # Multipart message
            for part in message_data['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
        else:
            # Simple message
            if 'data' in message_data['payload']['body']:
                return base64.urlsafe_b64decode(message_data['payload']['body']['data']).decode('utf-8')
        
        return "No plain text content found"
    except Exception as e:
        print(f"Error extracting email body: {e}")
        return "Error extracting email content"

def send_whatsapp_message(message_body, to_number):
    """Send WhatsApp message via Twilio"""
    try:
        twilio_sid = get_setting('twilio_sid')
        twilio_token = get_setting('twilio_token')
        twilio_whatsapp_number = get_setting('twilio_whatsapp_number')
        
        if not all([twilio_sid, twilio_token, twilio_whatsapp_number]):
            raise Exception("Twilio credentials not configured")
        
        client = Client(twilio_sid, twilio_token)
        
        message = client.messages.create(
            from_=f'whatsapp:{twilio_whatsapp_number}',
            body=message_body,
            to=f'whatsapp:{to_number}'
        )
        
        print(f"WhatsApp message sent: {message.sid}")
        return True
        
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")
        return False

def mark_email_as_read(service, message_id):
    """Mark email as read in Gmail"""
    try:
        service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
        print(f"Marked email {message_id} as read")
    except Exception as e:
        print(f"Error marking email as read: {e}")

def check_email_filters(subject, filters):
    """Check if email subject matches any filter keywords"""
    subject_lower = subject.lower()
    for keyword in filters:
        if keyword.lower() in subject_lower:
            return True
    return False

def process_emails():
    """Main function to process unread emails"""
    try:
        # Get configuration
        target_whatsapp_number = get_setting('target_whatsapp_number')
        filters = get_filters()
        
        if not target_whatsapp_number:
            print("Target WhatsApp number not configured")
            return
        
        if not filters:
            print("No filter keywords configured")
            return
        
        # Get Gmail service
        service = get_gmail_service()
        
        # Get unread messages
        results = service.users().messages().list(
            userId='me',
            labelIds=['UNREAD'],
            maxResults=10
        ).execute()
        
        messages = results.get('messages', [])
        
        if not messages:
            print("No unread messages found")
            return
        
        print(f"Found {len(messages)} unread messages")
        
        for message in messages:
            try:
                # Get full message details
                msg = service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='full'
                ).execute()
                
                # Extract headers
                headers = msg['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                thread_id = msg['threadId']
                
                print(f"Processing email: {subject}")
                
                # Check if subject matches filters
                if check_email_filters(subject, filters):
                    print(f"Email matches filters: {subject}")
                    
                    # Extract email body
                    email_body = extract_email_body(msg['payload'])
                    
                    # Create WhatsApp message with subject
                    whatsapp_message = f"Subject: {subject}\n\n{email_body}"
                    
                    # Send to WhatsApp
                    if send_whatsapp_message(whatsapp_message, target_whatsapp_number):
                        # Store conversation mapping
                        store_conversation_mapping(thread_id, target_whatsapp_number)
                        
                        # Mark email as read
                        mark_email_as_read(service, message['id'])
                        
                        print(f"Successfully forwarded email: {subject}")
                    else:
                        print(f"Failed to send WhatsApp message for: {subject}")
                else:
                    print(f"Email does not match filters: {subject}")
                    
            except Exception as e:
                print(f"Error processing message {message['id']}: {e}")
                continue
                
    except Exception as e:
        print(f"Error in process_emails: {e}")

def main():
    """Main worker loop"""
    print("Starting Gmail-to-WhatsApp worker...")
    
    while True:
        try:
            process_emails()
        except Exception as e:
            print(f"Error in main loop: {e}")
        
        # Wait 60 seconds before next check
        print("Waiting 60 seconds before next check...")
        time.sleep(60)

if __name__ == '__main__':
    main() 