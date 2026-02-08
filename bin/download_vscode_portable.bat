@echo off
setlocal EnableExtensions EnableDelayedExpansion

rem ------------------------------------------------------------
rem Read VS Code version from file
rem ------------------------------------------------------------

SET BIN_DIR=%~dp0
set VERSION_FILE=%BIN_DIR%vscode
SET LOCAL_PIXELPOUCH_DIR=%LOCALAPPDATA%\PixelPouch\

if not exist "%VERSION_FILE%" (
    echo ERROR: VERSION file not found: %VERSION_FILE%
    exit /b 1
)

set /p VERSION=<"%VERSION_FILE%"

if "%VERSION%"=="" (
    echo ERROR: VERSION is empty
    exit /b 2
)

rem ------------------------------------------------------------
rem Build download URL
rem ------------------------------------------------------------

set DOWNLOAD_URL=https://update.code.visualstudio.com/%VERSION%/win32-x64-archive/stable
set OUT_FILE=%LOCAL_PIXELPOUCH_DIR%VSCode-%VERSION%-win32-x64.zip
set DEST_DIR=%LOCAL_PIXELPOUCH_DIR%vscode

echo.
echo VS Code version : %VERSION%
echo Download URL    : %DOWNLOAD_URL%
echo Output file     : %OUT_FILE%
echo.

rem ------------------------------------------------------------
rem Download
rem ------------------------------------------------------------

echo [INFO] Downloading VS Code portable ZIP...
curl -L -o "%OUT_FILE%" "%DOWNLOAD_URL%"

if errorlevel 1 (
    echo ERROR: Download failed
    exit /b 3
)

rem ------------------------------------------------------------
rem Verify result
rem ------------------------------------------------------------

if not exist "%OUT_FILE%" (
    echo ERROR: Output file not found after download
    exit /b 4
)
echo [DONE] Download completed successfully.

echo [INFO] Extracting %OUT_FILE% to %DEST_DIR% ...

powershell -NoProfile -Command ^
  "Expand-Archive -Force '%OUT_FILE%' '%DEST_DIR%'"

if errorlevel 1 (
    echo ERROR: Failed to extract ZIP
    exit /b 2
)

endlocal
exit /b 0
