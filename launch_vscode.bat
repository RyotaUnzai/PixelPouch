@REM @echo off
@REM SETLOCAL ENABLEDELAYEDEXPANSION

SET PROJECT_ROOT=%~dp0
FOR %%I IN (.) DO SET PROJECT_NAME=%%~nxI
SET BIN_DIR=%PROJECT_ROOT%bin\


:: Set up DCC environment
SET HOUDINI_LOCATION=C:\Program Files\Side Effects Software\Houdini 21.0.512

:: Set up Rez environment
set REZ_PACKAGES_PATH=%PROJECT_ROOT%rez\packages;%PROJECT_ROOT%rez\projects

:: Set up VSCode environment
SET LOCAL_PIXELPOUCH_DIR=%LOCALAPPDATA%\PixelPouch\
set VSCODE_DIR=%LOCAL_PIXELPOUCH_DIR%vscode\
set VERSION_FILE=%BIN_DIR%vscode
set /p VERSION=<"%VERSION_FILE%"

if "%VERSION%"=="" (
    echo ERROR: VERSION is empty
    exit /b 2
)


if defined VSCODE_DIR (
    if not exist "%VSCODE_DIR%data" (
        echo [INFO] "%VSCODE_DIR%data" does not exist. creating...
        mkdir "%VSCODE_DIR%data"
    ) else (
        echo [INFO] "%VSCODE_DIR%" already exists.
    )
    powershell -ExecutionPolicy Bypass -File "%BIN_DIR%install_extensions.ps1"
    copy %PROJECT_ROOT%\bin\settings.json "%VSCODE_DIR%data\user-data\User\settings.json"

    echo Launching VSCode version %VERSION%...
    "%VSCODE_DIR%Code.exe" --new-window  %PROJECT_ROOT%.vscode\%PROJECT_NAME%.code-workspace
) else (
    echo No VSCode installation found in bin folder.
)

goto :eof


:CompareVersions


setlocal
set v1=%~1
set v2=%~2


for /f "tokens=1-3 delims=." %%a in ("%v1%") do (
    set v1a=000%%a
    set v1b=000%%b
    set v1c=000%%c
)
for /f "tokens=1-3 delims=." %%a in ("%v2%") do (
    set v2a=000%%a
    set v2b=000%%b
    set v2c=000%%c
)

set v1a=!v1a:~-3!
set v1b=!v1b:~-3!
set v1c=!v1c:~-3!
set v2a=!v2a:~-3!
set v2b=!v2b:~-3!
set v2c=!v2c:~-3!

set result=equal
if "!v1a!!v1b!!v1c!" GTR "!v2a!!v2b!!v2c!" set result=greater
if "!v1a!!v1b!!v1c!" LSS "!v2a!!v2b!!v2c!" set result=less

endlocal & set %3=%result%
goto :eof
