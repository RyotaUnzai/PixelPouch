param (
    [Parameter(Mandatory = $true)]
    [string]$SourceFile
)

# ---- validation -------------------------------------------------

if (-not (Test-Path $SourceFile)) {
    Write-Error "File not found: $SourceFile"
    exit 1
}

if ([System.IO.Path]::GetExtension($SourceFile) -ne ".py") {
    Write-Error "Not a Python file: $SourceFile"
    exit 1
}

# ---- paths ------------------------------------------------------

$sourcePath = Resolve-Path $SourceFile
$sourceDir = Split-Path $sourcePath
$baseName = [System.IO.Path]::GetFileNameWithoutExtension($sourcePath)
$targetStub = Join-Path $sourceDir "$baseName.pyi"
$scriptPath = Join-Path $PSScriptRoot "generate_ui_stub.py"

# ---- run stub generator -----------------------------------------

Write-Host "Generating stub for $sourcePath"

python $scriptPath $sourcePath $targetStub

if ($LASTEXITCODE -ne 0) {
    Write-Error "Stub generation failed"
    exit 2
}

Write-Host "Stub written to $targetStub"
