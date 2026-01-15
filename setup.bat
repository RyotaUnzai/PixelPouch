@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

SET PROJECT_ROOT=%~dp0
SET BIN_DIR=%PROJECT_ROOT%bin\
SET EMBED_PYTHON_DIR=%BIN_DIR%python-3.10.10-embed-amd64\
SET GET_PIP_PY_PATH=%BIN_DIR%get-pip.py

:: Set up Python environment
SET PYENV=%PROJECT_ROOT%\.pyenv\pyenv-win
SET PYENV_HOME=%PYENV%
SET PYENV_ROOT=%PYENV%
SET PATH=%PYENV%\shims;%PYENV%\bin;%PATH%

REM Copy .pth files
echo [SETUP] Seting embedded Python...
copy %BIN_DIR%python310._pth %EMBED_PYTHON_DIR%python310._pth 
copy %BIN_DIR%setup.pth %EMBED_PYTHON_DIR%setup.pth
echo [DONE] Set embedded Python successfully.

REM Install get-pip.py
echo [INSTALL] Installing get-pip.py...
curl -L https://bootstrap.pypa.io/get-pip.py -o %GET_PIP_PY_PATH%
%EMBED_PYTHON_DIR%python.exe %GET_PIP_PY_PATH%
echo [DONE] get-pip.py installed successfully.

REM Install modules into the embedded Python environment
echo [INSTALL] Installing pyenv...
%EMBED_PYTHON_DIR%python.exe -m pip install pyenv-win --target .pyenv
echo [DONE] pyenv installed successfully.

REM Install Python3.10.5 with pyenv
echo [INSTALL] Installing Python3.10.5 with pyenv...
cmd /c "%BIN_DIR%pyenv.bat"
IF ERRORLEVEL 1 (
  echo [ERROR] pyenv step failed.
  goto :EOF
)
echo [DONE] Python3.10.5 installed successfully.

REM Create virtual environment (.venv)
echo [CREATE] Creating .venv...
cmd /c "%BIN_DIR%venv.bat"
IF ERRORLEVEL 1 (
  echo [ERROR] venv step failed.
  goto :EOF
)
echo [DONE] .venv created successfully.

REM Activate the virtual environment and verify Python/pip paths
echo [INFO] Activating .venv and checking Python/pip paths...
call "%PROJECT_ROOT%.venv\Scripts\activate.bat"
where python
where pip
python -c "import sys; print(sys.executable)"


echo [UPGRADE] Upgrading pip...
"%PROJECT_ROOT%.venv\Scripts\python.exe" -m pip install --upgrade pip
IF ERRORLEVEL 1 (
  echo [ERROR] pip upgrade failed.
  goto :EOF
)
echo [DONE] pip upgraded successfully.

echo [INSTALL] Installing PySide6...
"%PROJECT_ROOT%.venv\Scripts\python.exe" -m pip install PySide6
"%PROJECT_ROOT%.venv\Scripts\python.exe" -m pip install PySide6-stubs
IF ERRORLEVEL 1 (
  echo [ERROR] PySide6 install failed.
  goto :EOF
)
echo [DONE] PySide6 installed successfully.

echo [INSTALL] Installing ruff...
"%PROJECT_ROOT%.venv\Scripts\python.exe" -m pip install ruff
IF ERRORLEVEL 1 (
  echo [ERROR] ruff install failed.
  goto :EOF
)
echo [DONE] ruff installed successfully.

echo [INSTALL] Installing mypy...
"%PROJECT_ROOT%.venv\Scripts\python.exe" -m pip install mypy
IF ERRORLEVEL 1 (
  echo [ERROR] mypy install failed.
  goto :EOF
)
echo [DONE] mypy installed successfully.
