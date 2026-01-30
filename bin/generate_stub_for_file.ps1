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

$tempDir = Join-Path $env:TEMP "stubgen_tmp_$([guid]::NewGuid())"

New-Item -ItemType Directory -Path $tempDir | Out-Null

# ---- run stubgen ------------------------------------------------

Write-Host "Generating stub for $sourcePath"

stubgen $sourcePath -o $tempDir | Out-Null

# ---- find generated pyi ----------------------------------------

$generatedStub = Get-ChildItem $tempDir -Recurse -Filter "$baseName.pyi" | Select-Object -First 1

if (-not $generatedStub) {
    Write-Error "Stub generation failed"
    Remove-Item $tempDir -Recurse -Force
    exit 2
}

# ---- move to source dir ----------------------------------------

$targetStub = Join-Path $sourceDir "$baseName.pyi"

Move-Item $generatedStub.FullName $targetStub -Force

Write-Host "Stub written to $targetStub"

# ---- cleanup ----------------------------------------------------

Remove-Item $tempDir -Recurse -Force
