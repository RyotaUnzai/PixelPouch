@REM @echo off
@REM SETLOCAL ENABLEDELAYEDEXPANSION

SET PROJECT_ROOT=%~dp0
FOR %%I IN (.) DO SET PROJECT_NAME=%%~nxI


:: Set up Python environment
SET PYENV=%PROJECT_ROOT%\.pyenv\pyenv-win
SET PYENV_HOME=%PYENV%
SET PYENV_ROOT=%PYENV%
SET PATH=%PYENV%\shims;%PYENV%\bin;%PATH%

:: Determine the latest version
SET MAX_VERSION=
SET MAX_PATH=

for /D %%D in ("%PROJECT_ROOT%\bin\VSCode-win32-x64-*") do (
    SET "DIR_NAME=%%~nxD"
    SET "VERSION=!DIR_NAME:VSCode-win32-x64-=!"

    REM Compare versions and find the highest one
    if not defined MAX_VERSION (
        SET "MAX_VERSION=!VERSION!"
        SET "MAX_PATH=%%D"
    ) else (
        call :CompareVersions "!VERSION!" "!MAX_VERSION!" result
        if "!result!"=="greater" (
            SET "MAX_VERSION=!VERSION!"
            SET "MAX_PATH=%%D"
        )
    )
)


if defined MAX_PATH (
    if not exist "%MAX_PATH%\data" (
        echo [INFO] "%MAX_PATH%\data" does not exist. creating...
        mkdir "%MAX_PATH%\data"
    ) else (
        echo [INFO] "%TARGET_PATH%" already exists.
    )
    powershell -ExecutionPolicy Bypass -File "%PROJECT_ROOT%\bin\install_extensions.ps1"
    copy %PROJECT_ROOT%\bin\settings.json "%MAX_PATH%\data\user-data\User\settings.json"

    echo Launching VSCode version %MAX_VERSION%...
    "%MAX_PATH%\Code.exe" --new-window  %PROJECT_ROOT%.vscode\%PROJECT_NAME%.code-workspace
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
