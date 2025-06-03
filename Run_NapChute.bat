@echo off

:: Lấy thư mục chứa file .bat
set "BATDIR=%~dp0"

:: Chuyển vào thư mục đó
cd /d "%BATDIR%"

:: Kiểm tra nếu môi trường ảo không tồn tại
if not exist "myenv\Scripts\activate.bat" (
    echo [Loi] Khong tim thay file kich hoat moi truong ao: myenv\Scripts\activate.bat
    pause
    exit /b
)

:: Kích hoạt môi trường ảo
call myenv\Scripts\activate.bat

:: Chạy script Python
python Nap_Chute.py

:: Giữ cửa sổ console để xem kết quả
pause

:: Tùy chọn: Chạy bằng PowerShell (chú thích)
@REM powershell -NoExit -Command "& {cd '%BATDIR%'; ./myenv/Scripts/Activate; python Nap_Chute.py}"