#!/usr/bin/env python3
"""
Test script to verify the Gmail-to-WhatsApp bridge setup
"""

import sqlite3
import os
import sys

def test_database():
    """Test database connectivity and schema"""
    print("Testing database...")
    try:
        conn = sqlite3.connect('config.db')
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['settings', 'filters', 'conversation_map']
        for table in required_tables:
            if table in tables:
                print(f"✓ Table '{table}' exists")
            else:
                print(f"✗ Table '{table}' missing")
                return False
        
        conn.close()
        print("✓ Database test passed")
        return True
        
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

def test_credentials_directory():
    """Test credentials directory"""
    print("Testing credentials directory...")
    try:
        if not os.path.exists('credentials'):
            os.makedirs('credentials')
            print("✓ Created credentials directory")
        else:
            print("✓ Credentials directory exists")
        return True
    except Exception as e:
        print(f"✗ Credentials directory test failed: {e}")
        return False

def test_dependencies():
    """Test if required packages are installed"""
    print("Testing dependencies...")
    required_packages = [
        'flask',
        'google-api-python-client',
        'google-auth-oauthlib',
        'twilio',
        'gunicorn'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print("✓ All dependencies are installed")
    return True

def test_configuration():
    """Test if basic configuration is set"""
    print("Testing configuration...")
    try:
        conn = sqlite3.connect('config.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT key, value FROM settings")
        settings = dict(cursor.fetchall())
        
        required_settings = [
            'twilio_sid',
            'twilio_token', 
            'twilio_whatsapp_number',
            'target_whatsapp_number'
        ]
        
        missing_settings = []
        for setting in required_settings:
            if setting in settings and settings[setting]:
                print(f"✓ {setting} is configured")
            else:
                print(f"✗ {setting} is not configured")
                missing_settings.append(setting)
        
        conn.close()
        
        if missing_settings:
            print("Configure missing settings in the web interface")
            return False
        
        print("✓ All required settings are configured")
        return True
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Gmail-to-WhatsApp Bridge Setup Test")
    print("=" * 40)
    
    tests = [
        test_dependencies,
        test_credentials_directory,
        test_database,
        test_configuration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! The application is ready to run.")
        print("\nNext steps:")
        print("1. Run: docker-compose up -d")
        print("2. Access: http://localhost:5000")
        print("3. Login with: ErmalAlija / Prishtina1997!")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == '__main__':
    main() 