# Gmail-to-WhatsApp Bridge Deployment Script for Windows
# Run this script in PowerShell as Administrator

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Gmail-to-WhatsApp Bridge Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "This script requires Administrator privileges. Please run PowerShell as Administrator." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Function to check if command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
if (Test-Command python) {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python is installed: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check pip
Write-Host "Checking pip..." -ForegroundColor Yellow
if (Test-Command pip) {
    Write-Host "✓ pip is available" -ForegroundColor Green
} else {
    Write-Host "✗ pip is not available" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Create credentials directory
Write-Host "Creating credentials directory..." -ForegroundColor Yellow
if (!(Test-Path "credentials")) {
    New-Item -ItemType Directory -Path "credentials" | Out-Null
    Write-Host "✓ Created credentials directory" -ForegroundColor Green
} else {
    Write-Host "✓ Credentials directory already exists" -ForegroundColor Green
}

# Initialize database
Write-Host "Initializing database..." -ForegroundColor Yellow
try {
    python -c "
import sqlite3
conn = sqlite3.connect('config.db')
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
print('Database initialized successfully')
"
    Write-Host "✓ Database initialized successfully" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to initialize database" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

# Check if Docker is available
Write-Host "Checking Docker availability..." -ForegroundColor Yellow
if (Test-Command docker) {
    Write-Host "✓ Docker is available" -ForegroundColor Green
    $useDocker = Read-Host "Docker is available. Would you like to use Docker deployment? (y/n)"
    if ($useDocker -eq "y" -or $useDocker -eq "Y") {
        Write-Host "Building Docker image..." -ForegroundColor Yellow
        try {
            docker build -t gmail-whatsapp-bridge .
            Write-Host "✓ Docker image built successfully" -ForegroundColor Green
            
            Write-Host "Starting application with Docker..." -ForegroundColor Yellow
            docker-compose up -d
            Write-Host "✓ Application started with Docker" -ForegroundColor Green
            Write-Host "Access the application at: http://localhost:5000" -ForegroundColor Cyan
        } catch {
            Write-Host "✗ Docker deployment failed" -ForegroundColor Red
            Write-Host $_.Exception.Message -ForegroundColor Red
        }
    }
} else {
    Write-Host "Docker not available, will use Python deployment" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($useDocker -ne "y" -and $useDocker -ne "Y") {
    Write-Host "To start the application manually:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Terminal 1 (Web Server):" -ForegroundColor White
    Write-Host "  python app.py" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Terminal 2 (Background Worker):" -ForegroundColor White
    Write-Host "  python worker.py" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Then open your browser to: http://localhost:5000" -ForegroundColor Cyan
}

Write-Host "Login credentials: ErmalAlija / Prishtina1997!" -ForegroundColor Yellow
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Access the web interface" -ForegroundColor White
Write-Host "2. Upload your Gmail credentials.json file" -ForegroundColor White
Write-Host "3. Configure your Twilio settings" -ForegroundColor White
Write-Host "4. Set up email filter keywords" -ForegroundColor White
Write-Host "5. Configure the Twilio webhook URL" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions, see deployment_guide.md" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Read-Host "Press Enter to exit" 