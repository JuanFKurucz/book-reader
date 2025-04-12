# PowerShell script to set up the PDF to Audiobook converter
Write-Host "Setting up PDF to Audiobook converter..." -ForegroundColor Green

# Create necessary directories
if (-not (Test-Path -Path "./books")) {
    Write-Host "Creating books directory..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path "./books" | Out-Null
}

if (-not (Test-Path -Path "./audiobooks")) {
    Write-Host "Creating audiobooks directory..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path "./audiobooks" | Out-Null
}

# Install dependencies
Write-Host "Installing required packages..." -ForegroundColor Cyan
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Create .env file if it doesn't exist
if (-not (Test-Path -Path "./.env")) {
    Write-Host "Creating .env file - please add your OpenAI API key later" -ForegroundColor Yellow
    "OPENAI_API_KEY=your_openai_api_key_here" | Out-File -FilePath "./.env"
    Write-Host "Note: Add your actual API key to the .env file" -ForegroundColor Red
} else {
    Write-Host ".env file already exists" -ForegroundColor Cyan
}

Write-Host "Setup complete! You can now run 'python main.py' to start the program." -ForegroundColor Green
Write-Host "For a quick test, try: 'python main.py --sample --max-pages 2'" -ForegroundColor Green
Write-Host "To format and lint code, run: 'ruff format .' and 'ruff check .'" -ForegroundColor Green
