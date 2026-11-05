@echo off
REM ===== Đóng gói Nhím KPI thành NhimKPI.exe (Windows) =====
chcp 65001 >nul
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements-build.txt
pyinstaller --noconfirm --clean --windowed --onedir ^
  --name NhimKPI ^
  --icon assets\nhim.ico ^
  --add-data "assets;assets" ^
  --collect-data customtkinter ^
  main.py
echo.
echo Xong! Phan mem nam o: dist\NhimKPI\NhimKPI.exe
echo Neu da cai Inno Setup, chay: iscc installer_windows.iss  de tao file Setup.exe
pause
