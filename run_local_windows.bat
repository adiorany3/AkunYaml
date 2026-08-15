@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    set "PY=py"
) else (
    where python >nul 2>nul
    if errorlevel 1 (
        echo Python tidak ditemukan.
        echo Install Python 3.10+ lalu jalankan file ini kembali.
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

echo [SETUP] Menjalankan ConvertYAML Local Runner...
".venv\Scripts\python.exe" local_runner.py --config local_config.json
if errorlevel 1 goto :error

echo.
echo Selesai. Cek akun.txt dan openclash_auto.yaml
pause
exit /b 0

:error
echo.
echo Proses gagal. Baca pesan error di atas.
pause
exit /b 1
