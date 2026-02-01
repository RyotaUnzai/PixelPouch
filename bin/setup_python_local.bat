@echo off


REM Verify Python 3.11.7 
SET PY_VERSION=3.11.7
SET LOCAL_PIXELPOUCH_DIR=%LOCALAPPDATA%\PixelPouch\
SET PYTHON_DIR=%LOCAL_PIXELPOUCH_DIR%python\tools\
SET PYTHON_EXE=%PYTHON_DIR%python.exe
SET NUGET=%LOCAL_PIXELPOUCH_DIR%nuget.exe

REM Download nuget.exe
echo [INFO] Downloading nuget.exe
if exist "%NUGET%" (
  echo nuget.exe already exists. Skipping download.
)  else (
  curl -L -o %LOCAL_PIXELPOUCH_DIR%nuget.exe https://dist.nuget.org/win-x86-commandline/latest/nuget.exe
)

IF ERRORLEVEL 1 (
  echo [ERROR] Failed to download nuget.exe
  goto :EOF
)
echo [DONE] nuget.exe downloaded succefully


REM Install python
echo [INFO] Downloading Python %PY_VERSION%
if exist "%LOCAL_PIXELPOUCH_DIR%python" (
    echo Existing Python found. Removing it...
    rmdir /s /q "%LOCAL_PIXELPOUCH_DIR%python"
)
echo Installing Python %PY_VERSION% via nuget..
%NUGET% install python -Version %PY_VERSION% -ExcludeVersion -OutputDirectory %LOCAL_PIXELPOUCH_DIR%

IF ERRORLEVEL 1 (
  echo [ERROR] Failed to install Python %PY_VERSION% 
  goto :EOF
)
echo [DONE] Python %PY_VERSION% downloaded successfully


popd
exit /b %ERR%
