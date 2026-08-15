@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    set "PY=py"
) else (
    where python >nul 2>nul
    if errorlevel 1 (
        echo Python 3 tidak ditemukan.
        pause
        exit /b 1
    )
    set "PY=python"
)

if not exist ".venv\Scripts\python.exe" (
    echo [SETUP] Membuat virtual environment...
    %PY% -m venv .venv
    if errorlevel 1 goto :error
)

".venv\Scripts\python.exe" local_runner.py --config local_config.json
if errorlevel 1 goto :error

echo.
echo Selesai.
pause
exit /b 0

:error
echo.
echo Proses gagal. Baca error di atas.
pause
exit /b 1
