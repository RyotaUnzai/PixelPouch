[CmdletBinding()]
param(
    [string]$ProjectRoot = "",
    [string]$ManifestPath = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$scriptRoot = if ($PSScriptRoot) {
    $PSScriptRoot
} else {
    Split-Path -Parent $MyInvocation.MyCommand.Path
}

if ([string]::IsNullOrWhiteSpace($ProjectRoot)) {
    $ProjectRoot = Split-Path -Parent $scriptRoot
}

if ([string]::IsNullOrWhiteSpace($ManifestPath)) {
    $ManifestPath = Join-Path $scriptRoot "resources_manifest.json"
}

$ProjectRoot = $ProjectRoot.Trim('"')
if ($ProjectRoot.EndsWith('\')) {
    $ProjectRoot = $ProjectRoot.TrimEnd('\')
}

$ManifestPath = $ManifestPath.Trim('"')

$ProjectRoot = [System.IO.Path]::GetFullPath($ProjectRoot)
$ResourcesRoot = Join-Path $ProjectRoot "python\pixelpouch\resources"
$ManagedIconRoot = Join-Path $ResourcesRoot "icons\fluent"
$ManagedLicenseRoot = Join-Path $ResourcesRoot "licenses\fluentui-system-icons"
$ManifestPath = [System.IO.Path]::GetFullPath($ManifestPath)

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message"
}

function Write-Step {
    param([string]$Message)
    Write-Host "[STEP] $Message"
}

function Write-Done {
    param([string]$Message)
    Write-Host "[DONE] $Message"
}

function Ensure-Directory {
    param([Parameter(Mandatory = $true)][string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
    }
}

function Reset-Directory {
    param([Parameter(Mandatory = $true)][string]$Path)
    if (Test-Path -LiteralPath $Path) {
        Remove-Item -LiteralPath $Path -Recurse -Force
    }
    Ensure-Directory -Path $Path
}

function Download-File {
    param(
        [Parameter(Mandatory = $true)][string]$Url,
        [Parameter(Mandatory = $true)][string]$Destination
    )

    Ensure-Directory -Path (Split-Path -Parent $Destination)

    & curl.exe -L --fail --silent --show-error --output $Destination $Url
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to download: $Url"
    }
}

if (-not (Test-Path -LiteralPath $ManifestPath)) {
    throw "Resource manifest not found: $ManifestPath"
}

Write-Step "Preparing resources at $ResourcesRoot"
Ensure-Directory -Path $ResourcesRoot
Reset-Directory -Path $ManagedIconRoot
Reset-Directory -Path $ManagedLicenseRoot

$manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
if (-not $manifest.entries) {
    throw "Resource manifest does not contain any entries: $ManifestPath"
}

foreach ($entry in $manifest.entries) {
    Write-Info "Processing resource pack: $($entry.name)"

    foreach ($fileEntry in $entry.files) {
        $destination = Join-Path $ResourcesRoot $fileEntry.destination
        Write-Info "Downloading: $($fileEntry.destination)"
        Download-File -Url $fileEntry.url -Destination $destination
    }

    foreach ($licenseEntry in $entry.license_files) {
        $destination = Join-Path $ResourcesRoot $licenseEntry.destination
        Write-Info "Downloading license: $($licenseEntry.destination)"
        Download-File -Url $licenseEntry.url -Destination $destination
    }
}

Write-Done "Resources are ready."
