# Setup script for Windows PowerShell

Write-Host "=" -NoNewline; Write-Host ("=" * 50)
Write-Host "LLM Quiz Solver - Setup Script"
Write-Host "=" -NoNewline; Write-Host ("=" * 50)
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Cyan
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python not found. Please install Python 3.9 or higher." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Cyan
if (Test-Path "venv") {
    Write-Host "  Virtual environment already exists" -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip --quiet
Write-Host "✓ Pip upgraded" -ForegroundColor Green

# Install requirements
Write-Host ""
Write-Host "Installing Python packages..." -ForegroundColor Cyan
Write-Host "  This may take a few minutes..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python packages installed" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install packages" -ForegroundColor Red
    exit 1
}

# Install Playwright browsers
Write-Host ""
Write-Host "Installing Playwright browsers..." -ForegroundColor Cyan
Write-Host "  This may take a few minutes..." -ForegroundColor Yellow
playwright install chromium
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Playwright browsers installed" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install browsers" -ForegroundColor Red
    exit 1
}

# Create .env file if it doesn't exist
Write-Host ""
Write-Host "Setting up environment configuration..." -ForegroundColor Cyan
if (Test-Path ".env") {
    Write-Host "  .env file already exists" -ForegroundColor Yellow
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "✓ .env file created from template" -ForegroundColor Green
    Write-Host ""
    Write-Host "  IMPORTANT: Edit .env file with your credentials!" -ForegroundColor Red
    Write-Host "  - Add your EMAIL" -ForegroundColor Yellow
    Write-Host "  - Add your SECRET" -ForegroundColor Yellow
    Write-Host "  - Add your OPENAI_API_KEY or ANTHROPIC_API_KEY" -ForegroundColor Yellow
}

# Create necessary directories
Write-Host ""
Write-Host "Creating directories..." -ForegroundColor Cyan
if (!(Test-Path "downloads")) {
    New-Item -ItemType Directory -Path "downloads" | Out-Null
}
Write-Host "✓ Directories created" -ForegroundColor Green

# Summary
Write-Host ""
Write-Host "=" -NoNewline; Write-Host ("=" * 50)
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "=" -NoNewline; Write-Host ("=" * 50)
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Edit .env file with your credentials" -ForegroundColor White
Write-Host "  2. Run: python test_system.py" -ForegroundColor White
Write-Host "  3. Run: python app.py" -ForegroundColor White
Write-Host "  4. Deploy to cloud platform" -ForegroundColor White
Write-Host ""
Write-Host "For deployment help, see DEPLOYMENT.md" -ForegroundColor Cyan
Write-Host "For prompt tips, see PROMPTS.md" -ForegroundColor Cyan
Write-Host ""
