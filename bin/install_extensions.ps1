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

# --- Auto-detect the latest portable VS Code in the same root as this script ---
$VSCodeFolders =
    Get-ChildItem -Path $ScriptRoot -Directory |
    Where-Object { $_.Name -like "VSCode-win32-x64-*" } |
    Sort-Object {
        # Parse version from folder name: VSCode-win32-x64-<version>
        $v = ($_.Name -replace '^VSCode-win32-x64-', '')
        try { [version]$v } catch { [version]'0.0.0' }
    } -Descending

if ($VSCodeFolders.Count -gt 0) {
    $Code = Join-Path $VSCodeFolders[0].FullName "bin\code.cmd"
    if (-not (Test-Path $Code)) {
        Write-Error "code.cmd not found under: $($VSCodeFolders[0].FullName)\bin"
        exit 1
    }
} else {
    # Optional fallback to PATH "code" if no portable folder found
    $CodeCmd = Get-Command code -ErrorAction SilentlyContinue
    if ($null -ne $CodeCmd) {
        $Code = $CodeCmd.Source
    } else {
        Write-Error "No VSCode-win32-x64-* folder found and 'code' not in PATH."
        exit 1
    }
}

Write-Host "Using VS Code CLI: $Code"

# --- Collect already installed extensions (ID@version) ---
$installedRaw = & $Code --list-extensions --show-versions
$installed = @{}
foreach ($line in $installedRaw) {
    if ($line -match '^(?<id>[^@]+)(@(?<ver>.+))?$') {
        $installed[$Matches.id.ToLower()] = $line.Trim()
    }
}

# --- Read targets from extensions.txt (ignore blanks and #comments) ---
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
