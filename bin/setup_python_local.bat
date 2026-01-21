@echo off


REM Verify Python 3.11.7 
SET PY_VERSION=3.11.7
SET BIN_DIR=%~dp0
SET PYTHON_DIR=%BIN_DIR%python\tools\
SET PYTHON_EXE=%PYTHON_DIR%python.exe

REM Download nuget.exe
echo [INFO] Downloading nuget.exe
if exist "%NUGET%" (
  echo nuget.exe already exists. Skipping download.
)  else (
  curl -L -o %BIN_DIR%nuget.exe https://dist.nuget.org/win-x86-commandline/latest/nuget.exe
)

IF ERRORLEVEL 1 (
  echo [ERROR] Failed to download nuget.exe
  goto :EOF
)
echo [DONE] nuget.exe downloaded succefully

REM Install python
echo [INFO] Downloading Python %PY_VERSION%
if exist "%BIN_DIR%python" (
    echo Existing Python found. Removing it...
    rmdir /s /q "%BIN_DIR%python"
)
echo Installing Python %PY_VERSION% via nuget..
%NUGET% install python -Version 3.11.7 -ExcludeVersion -OutputDirectory %BIN_DIR%

IF ERRORLEVEL 1 (
  echo [ERROR] Failed to install Python %PY_VERSION% 
  goto :EOF
)
echo [DONE] Python %PY_VERSION% downloaded successfully

REM Creating venv
echo [INFO] Using "%PYTHON_EXE%" to create venv at "%CD%\.venv"
if exist "%CD%\.venv" (
    echo Existing .venv found. Removing it...
    rmdir /s /q "%CD%\.venv"
)
echo [CREATE] Creating virtual environment .venv...
%PYTHON_EXE% -m venv .venv
set ERR=%ERRORLEVEL%
echo [DONE] .venv created successfully.

popd
exit /b %ERR%
