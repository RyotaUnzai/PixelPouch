# Bootstrap uv, create venv using fixed Python, install requirements.
# Designed to be called from setup.bat at project root.

$ErrorActionPreference = "Stop"

# ------------------------------------------------------------
# Resolve paths
# ------------------------------------------------------------

# bin/
$BinDir = $PSScriptRoot

# Project root (parent of bin/)
$ProjectRoot = Resolve-Path (Join-Path $BinDir "..")

# requirements files (in bin/)
$ReqDev = Join-Path $BinDir "requirements-dev.txt"
$ReqDcc = Join-Path $BinDir "requirements-dcc.txt"

foreach ($req in @($ReqDev, $ReqDcc)) {
    if (-not (Test-Path $req)) {
        Write-Error "Requirements file not found: $req"
        exit 1
    }
}

# venv (project root)
$VenvDir = Join-Path $ProjectRoot ".venv"

# fixed Python (nuget-installed)
$PythonExe = Join-Path $env:LOCALAPPDATA "PixelPouch\python\tools\python.exe"

Write-Host "Project root : $ProjectRoot"
Write-Host "Bin dir : $BinDir"
Write-Host "Python exe : $PythonExe"
Write-Host "Venv dir : $VenvDir"

# ------------------------------------------------------------
# Validate Python executable
# ------------------------------------------------------------

if (-not (Test-Path $PythonExe)) {
    Write-Error "Python executable not found: $PythonExe"
    exit 2
}

# ------------------------------------------------------------
# Ensure uv is installed (official installer)
# ------------------------------------------------------------

$UvCmd = Get-Command uv -ErrorAction SilentlyContinue

if ($null -eq $UvCmd) {
    Write-Host "uv not found. Installing via official installer..."

    try {
        Invoke-WebRequest https://astral.sh/uv/install.ps1 -UseBasicParsing | Invoke-Expression
    }
    catch {
        Write-Error "Failed to install uv"
        exit 3
    }

    # Refresh PATH for current session
    $env:PATH =
    [System.Environment]::GetEnvironmentVariable("PATH", "User") + ";" +
    [System.Environment]::GetEnvironmentVariable("PATH", "Machine")

    $UvCmd = Get-Command uv -ErrorAction SilentlyContinue
    if ($null -eq $UvCmd) {
        Write-Error "uv installation completed but 'uv' is still not available in PATH"
        exit 4
    }
}

Write-Host "Using uv: $($UvCmd.Source)"

# ------------------------------------------------------------
# Create virtual environment (always recreate, bat-compatible)
# ------------------------------------------------------------

Write-Host "[INFO] Using '$PythonExe' to create venv at '$VenvDir'"

if (Test-Path $VenvDir) {
    Write-Host "Existing .venv found. Removing it..."
    Remove-Item -Recurse -Force $VenvDir
}

Write-Host "[CREATE] Creating virtual environment .venv using uv..."
uv venv $VenvDir --python $PythonExe

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to create virtual environment with uv"
    exit 5
}

Write-Host "[DONE] .venv created successfully."

# ------------------------------------------------------------
# Activate virtual environment
# ------------------------------------------------------------

$ActivateScript = Join-Path $VenvDir "Scripts\Activate.ps1"
if (-not (Test-Path $ActivateScript)) {
    Write-Error "Virtual environment activation script not found: $ActivateScript"
    exit 6
}

. $ActivateScript
Write-Host "Virtual environment activated."

# ------------------------------------------------------------
# Install dependencies using uv
# ------------------------------------------------------------

Write-Host "Installing dependencies into virtual environment (.venv)..."
uv pip install -r $ReqDev

Write-Host "Installing dependencies into runtime environment (python\third_party)..."
uv pip install -r $ReqDcc --target (Join-Path $ProjectRoot "python\third_party")
Write-Host "All dependencies installed successfully."
