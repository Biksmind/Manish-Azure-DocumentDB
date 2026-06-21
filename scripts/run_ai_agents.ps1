[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$parentDir = (Resolve-Path (Join-Path $repoRoot "..")).Path
$companionRepoPath = Join-Path $parentDir "DocumentDB_Workshop_0906"
$agentsAppPath = Join-Path $companionRepoPath "4-AI-Agents\mobile-agents"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "git is required but was not found in PATH."
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "python is required but was not found in PATH."
}

if (-not (Test-Path $companionRepoPath)) {
    Write-Host "Companion repo not found. Cloning DocumentDB_Workshop_0906..."
    Push-Location $parentDir
    try {
        git clone https://github.com/Biksmind/DocumentDB_Workshop_0906.git
    }
    finally {
        Pop-Location
    }
}

if (-not (Test-Path $agentsAppPath)) {
    throw "AI agents app path was not found: $agentsAppPath"
}

Write-Host "Starting AI agents app from: $agentsAppPath"
Push-Location $agentsAppPath
try {
    python app.py
}
finally {
    Pop-Location
}
