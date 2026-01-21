@echo off


REM Verify Python 3.11.7 
SET BIN_DIR=%CD%\bin\
SET PYTHON_DIR=%BIN_DIR%python\tools\
SET PYTHON_EXE=%EMBED_PYTHON_DIR%python.exe

curl -L -o %BIN_DIR%nuget.exe https://dist.nuget.org/win-x86-commandline/latest/nuget.exe

%BIN_DIR%nuget.exe install python -Version 3.11.7 -ExcludeVersion -OutputDirectory %BIN_DIR%

echo [INFO] Using "%PYTHON_EXE%" to create venv at "%CD%\.venv"
echo [CREATE] Creating virtual environment .venv...
%PYTHON_EXE% -m venv .venv
set ERR=%ERRORLEVEL%
echo [DONE] .venv created successfully.

popd
exit /b %ERR%

