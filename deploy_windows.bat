@echo off
echo ========================================
echo Gmail-to-WhatsApp Bridge Deployment
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python is installed!
echo.

echo Checking pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip is not available
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo Dependencies installed successfully!
echo.

echo Creating credentials directory...
if not exist "credentials" mkdir credentials

echo Initializing database...
python -c "import sqlite3; conn = sqlite3.connect('config.db'); cursor = conn.cursor(); cursor.execute('CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)'); cursor.execute('CREATE TABLE IF NOT EXISTS filters (id INTEGER PRIMARY KEY AUTOINCREMENT, keyword TEXT UNIQUE)'); cursor.execute('CREATE TABLE IF NOT EXISTS conversation_map (thread_id TEXT PRIMARY KEY, whatsapp_user_number TEXT, last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'); conn.commit(); conn.close(); print('Database initialized successfully')"

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the application:
echo.
echo Terminal 1 (Web Server):
echo   python app.py
echo.
echo Terminal 2 (Background Worker):
echo   python worker.py
echo.
echo Then open your browser to: http://localhost:5000
echo Login: ErmalAlija / Prishtina1997!
echo.
echo ========================================
pause 