@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

SET PROJECT_ROOT=%~dp0
SET BIN_DIR=%PROJECT_ROOT%bin\
SET GET_PIP_PY_PATH=%BIN_DIR%get-pip.py
SET PY_VERSION=3.11.7
SET LOCAL_PYTHON_DIR=%BIN_DIR%python\tools\
SET LOCAL_PYTHON_EXE=%LOCAL_PYTHON_DIR%python.exe
SET NUGET=%BIN_DIR%nuget.exe

:: Set up DCC environment
SET HOUDINI_LOCATION="C:\Program Files\Side Effects Software\Houdini 21.0.512\"

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
