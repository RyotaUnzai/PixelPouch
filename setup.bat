@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

SET PROJECT_ROOT=%~dp0
SET BIN_DIR=%PROJECT_ROOT%bin\
SET PYTHON_DIR=%BIN_DIR%python\tools\
SET GET_PIP_PY_PATH=%BIN_DIR%get-pip.py

:: Set up DCC environment
SET HOUDINI_INSTALLATION_DIR="C:\Program Files\Side Effects Software\Houdini 21.0.512\"

@REM :: Set up Python environment
@REM SET PYENV=%PROJECT_ROOT%\.pyenv\pyenv-win
@REM SET PYENV_HOME=%PYENV%
@REM SET PYENV_ROOT=%PYENV%
@REM SET PATH=%PYENV%\shims;%PYENV%\bin;%PATH%
SET PYTHON_EXE=%EMBED_PYTHON_DIR%python.exe

REM Copy .pth files
@REM echo [SETUP] Seting embedded Python...
@REM copy %BIN_DIR%python311._pth %EMBED_PYTHON_DIR%python311._pth 
@REM copy %BIN_DIR%setup.pth %EMBED_PYTHON_DIR%setup.pth
@REM echo [DONE] Set embedded Python successfully.

@REM REM Install get-pip.py
@REM echo [INSTALL] Installing get-pip.py...
@REM curl -L https://bootstrap.pypa.io/get-pip.py -o %GET_PIP_PY_PATH%
@REM %EPYTHON_EXER% %GET_PIP_PY_PATH%
@REM echo [DONE] get-pip.py installed successfully.


@REM echo [INSTALL] Installing virtualenv...
@REM %EPYTHON_EXER% -m pip install virtualenv
@REM echo [DONE] Installed virtualenv successfully.


@REM REM Install modules into the embedded Python environment
@REM echo [INSTALL] Installing pyenv...
@REM %EMBED_PYTHON_DIR%python.exe -m pip install pyenv-win --target .pyenv
@REM echo [DONE] pyenv installed successfully.

@REM REM Install Python3.11.7 with pyenv
@REM echo [INSTALL] Installing Python3.11.7 with pyenv...
@REM cmd /c "%BIN_DIR%pyenv.bat"
@REM IF ERRORLEVEL 1 (
@REM   echo [ERROR] pyenv step failed.
@REM   goto :EOF
@REM )
@REM echo [DONE] Python3.11.7 installed successfully.

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

echo [INSTALL] Installing types-houdini...
"%PROJECT_ROOT%.venv\Scripts\python.exe" -m pip install types-houdini
IF ERRORLEVEL 1 (
  echo [ERROR] types-houdini install failed.
  goto :EOF
)
echo [DONE] types-houdini installed successfully.

echo [INSTALL] Installing debugpy...
"%PROJECT_ROOT%.venv\Scripts\python.exe" -m pip install debugpy
IF ERRORLEVEL 1 (
  echo [ERROR] debugpy install failed.
  goto :EOF
)
echo [DONE] debugpy installed successfully.

echo [INSTALL] Installing pyyaml...
"%PROJECT_ROOT%.venv\Scripts\python.exe" -m pip install pyyaml
IF ERRORLEVEL 1 (
  echo [ERROR] pyyaml install failed.
  goto :EOF
)
echo [DONE] pyyaml installed successfully.


REM Install Python packages for Houdini using Houdini's bundled Python
echo [ISTALL] Installing debugpy for Houdini...
%HOUDINI_INSTALLATION_DIR%python311\python.exe -m pip install debugpy --target %PROJECT_ROOT%\python\third_party
IF ERRORLEVEL 1 (
  echo [ERROR] debugpy install failed.
  goto :EOF
)
echo [DONE] debugpy installed successfully.

echo [ISTALL] Installing pyyaml for Houdini...
%HOUDINI_INSTALLATION_DIR%python311\python.exe -m pip install debugpy --target %PROJECT_ROOT%\python\third_party
IF ERRORLEVEL 1 (
  echo [ERROR] pyyaml install failed.
  goto :EOF
)
echo [DONE] pyyaml installed successfully.
