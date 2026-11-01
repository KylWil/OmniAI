@echo off
setlocal

cd /d "%~dp0"

:: ---------- Prerequisites (fail fast) ----------

where java >nul 2>&1 || (echo Java not found. Please install Java first. & pause & exit /b 1)
if not exist "requirements.txt" (echo requirements.txt not found next to this script. & pause & exit /b 1)

where uv >nul 2>&1
if errorlevel 1 (
  echo Installing uv...
  powershell -NoProfile -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" || (echo uv install failed. & pause & exit /b 1)
  set "PATH=%USERPROFILE%\.local\bin;%PATH%"
)
where uv >nul 2>&1 || (echo uv not found after install. Restart the terminal and re-run. & pause & exit /b 1)

:: ---------- Python venv ----------

if not exist ".venv\Scripts\python.exe" (
  uv venv --seed --python 3.12 .venv || (echo Failed to create venv. & pause & exit /b 1)
)
set "PY=%~dp0.venv\Scripts\python.exe"

:: ---------- Detect GPU ----------

set "GPU=other"
powershell -NoProfile -command "if (Get-CimInstance Win32_VideoController | Where-Object { $_.Name -match 'Radeon.*RX\s?[79]\d{3}' }) { exit 0 } else { exit 1 }"
if not errorlevel 1 set "GPU=amd"
nvidia-smi >nul 2>&1
if not errorlevel 1 set "GPU=nvidia"

:: ---------- Install torch ----------

if "%GPU%"=="amd" (
  echo AMD RX 7000/9000 GPU detected, installing ROCm build of torch.
  call :install_torch_amd || (echo torch install failed. & pause & exit /b 1)
) else (
  echo Installing torch, auto-detecting NVIDIA CUDA or CPU.
  uv pip install --python "%PY%" torch --torch-backend=auto || (echo torch install failed. & pause & exit /b 1)
)

uv pip install --python "%PY%" -r requirements.txt || (echo Package install failed. & pause & exit /b 1)

:: ---------- FightingICE ----------

set "BASE=https://github.com/TeamFightingICE/FightingICE/releases/download/v7.1"

curl -fL -o "DareFightingICE-7.1.zip" "%BASE%/DareFightingICE-7.1.zip" || (echo Download failed. & pause & exit /b 1)
curl -fL -o "resource-7.1.zip" "%BASE%/resource-7.1.zip" || (echo Download failed. & pause & exit /b 1)

tar -xf "DareFightingICE-7.1.zip" || (echo Extraction failed. & pause & exit /b 1)
if not exist "FightingICE7.1" mkdir "FightingICE7.1"
tar -xf "resource-7.1.zip" -C "FightingICE7.1" || (echo Extraction failed. & pause & exit /b 1)

del /f /q "DareFightingICE-7.1.zip" "resource-7.1.zip" 2>nul

cd /d "FightingICE7.1" || (echo FightingICE7.1 folder not found. & pause & exit /b 1)

del /f /q "run-linux-amd64.sh" "run-macos-arm64.sh" "run-windows-amd64.bat" 2>nul

(
  echo @ECHO OFF
  echo java -cp FightingICE.jar;./lib/*;./lib/lwjgl/*;./lib/lwjgl/natives/windows/amd64/*;./lib/grpc/*; Main --limithp 400 400 --grey-bg --pyftg-mode
  echo pause
) > "run-windows.bat"

(
  echo @ECHO OFF
  echo java -cp FightingICE.jar;./lib/*;./lib/lwjgl/*;./lib/lwjgl/natives/windows/amd64/*;./lib/grpc/*; Main --limithp 400 400 --grey-bg --pyftg-mode --input-sync --headless-mode
  echo pause
) > "run-windows-headless.bat"

exit /b 0

:: ---------- Subroutines ----------

:install_torch_amd
set "ROCM=https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1"
uv pip install --python "%PY%" ^
  "%ROCM%/rocm_sdk_core-7.2.1-py3-none-win_amd64.whl" ^
  "%ROCM%/rocm_sdk_devel-7.2.1-py3-none-win_amd64.whl" ^
  "%ROCM%/rocm_sdk_libraries_custom-7.2.1-py3-none-win_amd64.whl" ^
  "%ROCM%/rocm-7.2.1.tar.gz" || exit /b 1
uv pip install --python "%PY%" "%ROCM%/torch-2.9.1%%2Brocm7.2.1-cp312-cp312-win_amd64.whl" || exit /b 1
exit /b 0