param (
    [Parameter(Mandatory = $true)]
    [string]$InputFile
)

# ------------------------------------------------------------
# validation
# ------------------------------------------------------------

if (-not (Test-Path $InputFile)) {
    Write-Error "File not found: $InputFile"
    exit 1
}

$inputPath = Resolve-Path $InputFile
$inputDir = Split-Path $inputPath
$ext = [System.IO.Path]::GetExtension($inputPath).ToLower()
$baseName = [System.IO.Path]::GetFileNameWithoutExtension($inputPath)

# ------------------------------------------------------------
# resolve ui file
# ------------------------------------------------------------

switch ($ext) {
    ".ui" {
        $uiPath = $inputPath
    }
    ".py" {
        $candidateUi = Join-Path $inputDir "$baseName.ui"
        if (-not (Test-Path $candidateUi)) {
            Write-Error "Corresponding .ui file not found: $candidateUi"
            exit 2
        }
        $uiPath = Resolve-Path $candidateUi
    }
    default {
        Write-Error "Unsupported file type: $InputFile"
        exit 3
    }
}

$uiDir = Split-Path $uiPath
$pyFile = Join-Path $uiDir "$baseName.py"

Write-Host "Resolved UI file: $uiPath"

# ------------------------------------------------------------
# step 1: ui -> py
# ------------------------------------------------------------

Write-Host "=== Step 1: Convert .ui to .py ==="
& "$PSScriptRoot/generate_py_from_ui.ps1" $uiPath

if ($LASTEXITCODE -ne 0) {
    Write-Error "UI to PY conversion failed"
    exit 4
}

if (-not (Test-Path $pyFile)) {
    Write-Error "Expected .py file not found: $pyFile"
    exit 5
}

# ------------------------------------------------------------
# step 2: py -> pyi
# ------------------------------------------------------------

Write-Host "=== Step 2: Generate .pyi stub ==="
& "$PSScriptRoot/generate_stub_for_file.ps1" $pyFile

if ($LASTEXITCODE -ne 0) {
    Write-Error "Stub generation failed"
    exit 6
}

Write-Host "=== Done: .py and .pyi generated successfully ==="
