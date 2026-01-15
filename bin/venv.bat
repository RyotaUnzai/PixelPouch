@echo off

REM Go up one directory from bin\venv.bat to the project root
pushd "%~dp0.."

REM Verify Python 3.10.5 is installed for pyenv
set PYENV_HOME=%CD%\.pyenv\pyenv-win
set PY310=%PYENV_HOME%\versions\3.10.5\python.exe
if exist "%PY310%" (
  set PYTHON_EXE=%PY310%
) else (
  echo [ERROR] Python 3.10.5 for pyenv was not found.
  goto :EOF
)

echo [INFO] Using "%PYTHON_EXE%" to create venv at "%CD%\.venv"
echo [CREATE] Creating virtual environment .venv...
%PYTHON_EXE% -m venv .venv
set ERR=%ERRORLEVEL%
echo [DONE] .venv created successfully.

popd
exit /b %ERR%