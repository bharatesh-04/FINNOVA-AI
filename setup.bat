@echo off
REM Finnova AI - Setup Script for Windows

echo 🚀 Finnova AI - Setup Script
echo ================================

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose are installed

REM Create .env file if it doesn't exist
if not exist "backend\.env" (
    echo 📝 Creating .env file...
    copy backend\.env.example backend\.env
    echo ⚠️  Please update backend\.env with your configuration
)

REM Build and start services
echo 🐳 Building and starting Docker services...
docker-compose up -d

REM Wait for database to be ready
echo ⏳ Waiting for database to be ready...
timeout /t 10 /nobreak

echo.
echo ✅ Setup complete!
echo.
echo 🎉 Finnova AI is now running:
echo    Frontend:  http://localhost:3000
echo    Backend:   http://localhost:8000
echo    API Docs:  http://localhost:8000/docs
echo.
echo 🚀 Next steps:
echo    1. Open http://localhost:3000 in your browser
echo    2. Register a new account
echo    3. Start tracking your expenses!
echo.
pause
