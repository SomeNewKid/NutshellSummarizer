$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$HostPython = "C:\Users\somen\AppData\Local\Programs\Python\Python311\python.exe"
$VenvWindowsPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$VenvUnixPython = Join-Path $ProjectRoot ".venv\bin\python.exe"
$AgentCoreCdkRoot = Join-Path $ProjectRoot "agentcore\cdk"

Set-Location $ProjectRoot

if (-not (Test-Path $HostPython)) {
    throw "Expected Python 3.11 executable was not found at $HostPython."
}

if (-not ((Test-Path $VenvWindowsPython) -or (Test-Path $VenvUnixPython))) {
    & $HostPython -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        throw "Virtual environment creation failed with exit code $LASTEXITCODE."
    }
}

if (Test-Path $VenvWindowsPython) {
    $VenvPython = $VenvWindowsPython
} elseif (Test-Path $VenvUnixPython) {
    $VenvPython = $VenvUnixPython
} else {
    throw "Could not find a Python executable in the virtual environment."
}

function Invoke-Pip {
    & $VenvPython -m pip @args
    if ($LASTEXITCODE -ne 0) {
        throw "pip command failed with exit code $LASTEXITCODE."
    }
}

function Invoke-CommandLine {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Command,

        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]] $Arguments
    )

    & $Command @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$Command $($Arguments -join ' ') failed with exit code $LASTEXITCODE."
    }
}

Invoke-Pip install --upgrade pip
Invoke-Pip install --editable ".[dev]"

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    throw "Node.js was not found. Install Node.js 20 or later before running AgentCore commands."
}

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    throw "npm was not found. Install Node.js 20 or later before running AgentCore commands."
}

if (-not (Get-Command agentcore -ErrorAction SilentlyContinue)) {
    throw "AgentCore CLI was not found. Install it with: npm install -g @aws/agentcore"
}

if (-not (Test-Path (Join-Path $AgentCoreCdkRoot "package-lock.json"))) {
    throw "Expected AgentCore CDK package lock file was not found."
}

Push-Location $AgentCoreCdkRoot
try {
    Invoke-CommandLine npm ci
    Invoke-CommandLine npm run build
}
finally {
    Pop-Location
}
