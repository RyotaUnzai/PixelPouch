@echo off

REM bin\venv.bat から見て ひとつ上 = プロジェクトルートへ移動
pushd "%~dp0.."


echo [INFO] Setting local Python version to 3.10.5
pyenv install 3.10.5
pyenv local 3.10.5
echo [DONE] Local Python version set to 3.10.5 successfully.