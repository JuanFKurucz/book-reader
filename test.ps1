# Test script for PDF to audiobook conversion
# Runs the converter with the sample PDF and limited pages

Write-Host "PDF to Audiobook Converter - Test Script" -ForegroundColor Green
Write-Host "-----------------------------------------" -ForegroundColor Green

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Cyan
$pythonVersion = python --version
Write-Host $pythonVersion

# Make sure the audiobooks directory exists
if (-not (Test-Path -Path "./audiobooks")) {
    Write-Host "Creating audiobooks directory..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path "./audiobooks"
}

# Ensure books directory exists and has the sample PDF
if (-not (Test-Path -Path "./books")) {
    Write-Host "Creating books directory..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path "./books"
    Write-Host "Please add sample.pdf to the books directory." -ForegroundColor Yellow
    exit
}

if (-not (Test-Path -Path "./books/sample.pdf")) {
    Write-Host "Error: sample.pdf not found in the books directory." -ForegroundColor Red
    Write-Host "Please add sample.pdf to the books directory before running this test." -ForegroundColor Yellow
    exit
}

# Run the converter with the sample PDF, 2 pages, and specific voice/model
Write-Host "Testing PDF to audiobook conversion with sample.pdf..." -ForegroundColor Green
Write-Host "Settings: 2 pages, 'alloy' voice, 'tts-1' model" -ForegroundColor Cyan

# Execute the command
python main.py --sample --max-pages 2 --voice alloy --model tts-1

# Verify results
if ($LASTEXITCODE -eq 0) {
    Write-Host "Test completed successfully." -ForegroundColor Green
} else {
    Write-Host "Test encountered errors. Please check the output above." -ForegroundColor Red
}
