@echo off
REM Download fonts for PixelPouch Houdini project
REM This script downloads fonts to ...\PixelPouch\houdini\fonts

setlocal enabledelayedexpansion

REM Define the target directory relative to script location
REM Script location: ...\PixelPouch\bin\download_fonts.bat
REM Target: ...\PixelPouch\houdini\fonts
set "SCRIPT_DIR=%~dp0"
for %%A in ("!SCRIPT_DIR!..") do set "PARENT_DIR=%%~fA"
set "FONT_DIR=!PARENT_DIR!\houdini\fonts"

REM Create the fonts directory if it doesn't exist
if not exist "!FONT_DIR!" (
    mkdir "!FONT_DIR!"
    echo Created directory: !FONT_DIR!
)

echo.
echo ==========================================
echo Starting font download...
echo Target directory: !FONT_DIR!
echo ==========================================
echo.

REM Download NotoSansCJKjp-Regular
echo Downloading: NotoSansCJKjp-Regular.otf
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://github.com/notofonts/noto-cjk/raw/main/Sans/OTF/Japanese/NotoSansCJKjp-Regular.otf', '!FONT_DIR!\NotoSansCJKjp-Regular.otf')"
if %ERRORLEVEL% equ 0 (
    echo [OK] NotoSansCJKjp-Regular.otf
) else (
    echo [FAILED] NotoSansCJKjp-Regular.otf
)

REM Download JetBrainsMono-Regular
echo Downloading: JetBrainsMono-Regular.ttf
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/JetBrainsMono-Regular.ttf', '!FONT_DIR!\JetBrainsMono-Regular.ttf')"
if %ERRORLEVEL% equ 0 (
    echo [OK] JetBrainsMono-Regular.ttf
) else (
    echo [FAILED] JetBrainsMono-Regular.ttf
)

REM Download Noto Sans JP Bold from noto-cjk
echo Downloading: NotoSansCJKjp-Bold.otf
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://github.com/notofonts/noto-cjk/raw/main/Sans/OTF/Japanese/NotoSansCJKjp-Bold.otf', '!FONT_DIR!\NotoSansCJKjp-Bold.otf')"
if %ERRORLEVEL% equ 0 (
    echo [OK] NotoSansCJKjp-Bold.otf
) else (
    echo [FAILED] NotoSansCJKjp-Bold.otf
)

echo.
echo ==========================================
echo Download complete!
echo Font directory: !FONT_DIR!
echo ==========================================
echo.
dir /b "!FONT_DIR!"
echo.
