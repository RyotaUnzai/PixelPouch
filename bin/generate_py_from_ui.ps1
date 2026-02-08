param (
    [Parameter(Mandatory = $true)]
    [string]$UiFile
)

# ---- validation -------------------------------------------------

if (-not (Test-Path $UiFile)) {
    Write-Error "File not found: $UiFile"
    exit 1
}

if ([System.IO.Path]::GetExtension($UiFile) -ne ".ui") {
    Write-Error "Not a .ui file: $UiFile"
    exit 1
}

# ---- paths ------------------------------------------------------

$uiPath = Resolve-Path $UiFile
$uiDir = Split-Path $uiPath
$baseName = [System.IO.Path]::GetFileNameWithoutExtension($uiPath)

$outPy = Join-Path $uiDir "ui_$baseName.py"

# ---- run pyside6-uic --------------------------------------------

Write-Host "Generating Python file from UI:"
Write-Host "  UI : $uiPath"
Write-Host "  PY : $outPy"

pyside6-uic $uiPath -o $outPy

if ($LASTEXITCODE -ne 0) {
    Write-Error "pyside6-uic failed"
    exit 2
}

Write-Host "Generated $outPy successfully"
