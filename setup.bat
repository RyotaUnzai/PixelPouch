@REM @echo off
@REM SETLOCAL ENABLEDELAYEDEXPANSION

SET PROJECT_ROOT=%~dp0
SET BIN_DIR=%PROJECT_ROOT%bin\
SET LOCAL_PIXELPOUCH_DIR=%LOCALAPPDATA%\PixelPouch\
SET GET_PIP_PY_PATH=%LOCALAPPDATA%\get-pip.py
SET PY_VERSION=3.11.7
SET LOCAL_PYTHON_DIR=%BIN_DIR%python\tools\
SET LOCAL_PYTHON_EXE=%LOCAL_PYTHON_DIR%python.exe
SET NUGET=%LOCALAPPDATA%nuget.exe

:: Clean up LOCAL_PIXELPOUCH_DIR
if defined LOCAL_PIXELPOUCH_DIR (
    echo Cleaning: "%LOCAL_PIXELPOUCH_DIR%"
    if exist "%LOCAL_PIXELPOUCH_DIR%\" (
        rem --- delete files ---
        del /q "%LOCAL_PIXELPOUCH_DIR%\*" >nul 2>&1

        rem --- delete subdirectories ---
        for /d %%D in ("%LOCAL_PIXELPOUCH_DIR%\*") do (
            rmdir /s /q "%%D" >nul 2>&1
        )
    ) else (
        mkdir "%LOCAL_PIXELPOUCH_DIR%"
    )
)   else (
    echo ERROR: LOCAL_PIXELPOUCH_DIR is not defined
    exit /b 1
)


:: Set up DCC environment
SET HOUDINI_LOCATION="C:\Program Files\Side Effects Software\Houdini 21.0.512\"



REM Download VSCode
echo [STEP] Downloading VSCode
cmd /c "%BIN_DIR%download_vscode_portable.bat"
IF ERRORLEVEL 1 (
  echo [ERROR] VSCode local setup failed
  goto :EOF
)
echo [DONE] VSCode local setup completed



REM Run Ptython local setup and venv creation
echo [STEP] Running Python local setup (create .venv)
cmd /c "%BIN_DIR%setup_python_local.bat"
IF ERRORLEVEL 1 (
  echo [ERROR] Python local setup failed
  goto :EOF
)
echo [DONE] Python local setup completed


REM Activate the virtual environment and verify Python/pip paths
set PYTHON_EXE=%PROJECT_ROOT%.venv\Scripts\python.exe
echo [INFO] Using Python:
"%PYTHON_EXE%" -c "import sys; print(sys.executable)"

echo [INFO] Using pip:
"%PYTHON_EXE%" -m pip --version

REM Install Python dependencies

echo [UPGRADE] Upgrading pip...
"%PYTHON_EXE%" -m pip install --upgrade pip
IF ERRORLEVEL 1 (
  echo [ERROR] Failed to upgrade pip.
  goto :EOF
)

echo [INSTALL] Installing Python development dependencies...
"%PYTHON_EXE%" -m pip install -r %BIN_DIR%requirements-dev.txt
IF ERRORLEVEL 1 (
  echo [ERROR] Failed to install development dependencies.
  goto :EOF
)

echo [CLEAN] Cleaning DCC third-party directory...
if exist "%PROJECT_ROOT%\python\third_party" (
  rmdir /s /q "%PROJECT_ROOT%\python\third_party"
)
mkdir "%PROJECT_ROOT%\python\third_party"

echo [INSTALL] Installing Python DCC tool dependencies...
"%PYTHON_EXE%" -m pip install -r %BIN_DIR%requirements-dcc.txt --target "%PROJECT_ROOT%\python\third_party"
IF ERRORLEVEL 1 (
  echo [ERROR] Failed to install DCC tool dependencies.
  goto :EOF
)

echo [DONE] Python dependencies installed successfully.
