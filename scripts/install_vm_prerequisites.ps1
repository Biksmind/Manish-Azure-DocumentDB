# Installs workshop prerequisites on a Windows VM using winget.
# Run in an elevated PowerShell terminal.

$ErrorActionPreference = 'Stop'

function Test-Command {
    param([string]$Name)
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

if (-not (Test-Command 'winget')) {
    Write-Error "winget is required but not found. Install App Installer from Microsoft Store and re-run this script."
}

$packages = @(
    @{ Id = 'Microsoft.VisualStudioCode'; Name = 'VS Code' },
    @{ Id = 'Python.Python.3.10'; Name = 'Python 3.10+' },
    @{ Id = 'MongoDB.Shell'; Name = 'mongosh' },
    @{ Id = 'Git.Git'; Name = 'Git' }
)

foreach ($pkg in $packages) {
    Write-Host "Installing $($pkg.Name)..." -ForegroundColor Cyan
    winget install --id $pkg.Id --exact --source winget --silent --accept-package-agreements --accept-source-agreements
}

Write-Host "\nVerifying installed tools..." -ForegroundColor Green

if (Test-Command 'code') {
    $v = (code --version | Select-Object -First 1)
    Write-Host "VS Code: $v"
} else {
    Write-Host "VS Code command not found in PATH yet. Restart terminal or sign out/in."
}

if (Test-Command 'python') {
    $v = (python --version)
    Write-Host "Python: $v"
} else {
    Write-Host "Python command not found in PATH yet. Restart terminal or sign out/in."
}

if (Test-Command 'mongosh') {
    $v = (mongosh --version)
    Write-Host "mongosh: $v"
} else {
    Write-Host "mongosh command not found in PATH yet. Restart terminal or sign out/in."
}

if (Test-Command 'git') {
    $v = (git --version)
    Write-Host "Git: $v"
} else {
    Write-Host "git command not found in PATH yet. Restart terminal or sign out/in."
}

Write-Host "\nPrerequisite setup complete." -ForegroundColor Green
