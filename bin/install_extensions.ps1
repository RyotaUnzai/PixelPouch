# install-extensions.ps1
# Run independent of the current working directory.
# Uses the folder of this script ($PSScriptRoot) as the root.

$ErrorActionPreference = "Stop"

# --- Resolve script root and input file ---
$ScriptRoot = $PSScriptRoot
$ListFile   = Join-Path $ScriptRoot "extensions.txt"

if (-not (Test-Path $ListFile)) {
    Write-Error "extensions.txt not found: $ListFile"
    exit 1
}

# Resolve VS Code (portable, fixed location)
$VSCodeRoot = Join-Path $env:LOCALAPPDATA "PixelPouch\vscode"
$Code       = Join-Path $VSCodeRoot "bin\code.cmd"

if (-not (Test-Path $Code)) {
    Write-Error "VS Code CLI not found: $Code"
    exit 1
}

Write-Host "Using VS Code CLI: $Code"

# Collect already installed extensions (ID@version)
$installedRaw = & $Code --list-extensions --show-versions
$installed = @{}

foreach ($line in $installedRaw) {
    if ($line -match '^(?<id>[^@]+)(@(?<ver>.+))?$') {
        $installed[$Matches.id.ToLower()] = $line.Trim()
    }
}

# Read targets from extensions.txt (ignore blanks and #comments)
$targets =
    Get-Content -LiteralPath $ListFile |
    ForEach-Object { $_.Trim() } |
    Where-Object { $_ -and (-not $_.StartsWith('#')) }

foreach ($ext in $targets) {
    if ($ext -match '^(?<id>[^@]+)(@(?<ver>.+))?$') {
        $id = $Matches.id.ToLower()

        if ($installed.ContainsKey($id)) {
            Write-Host "✓ Already installed: $($installed[$id])" -ForegroundColor DarkGray
            continue
        }

        Write-Host "→ Installing: $ext"
        & $Code --install-extension $ext
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "Failed to install: $ext"
        }
    }
}

Write-Host "Done."
