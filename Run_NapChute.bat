@echo off

:: Lấy thư mục chứa file .bat
set BATDIR=%~dp0

:: Chuyển vào thư mục đó
cd /d %BATDIR% 

:: Kích hoạt môi trường ảo
call myenv\Scripts\activate.bat

:: Chạy script Python
python Nap_Chute.py

:: E:
:: cd E:\App_Load_code_STM32
:: call E:\App_Load_code_STM32\myenv\Scripts\Activate
:: python Nap_Chute.py

pause

@REM powershell -NoExit -Command "& {cd 'E:\App_Load_code_STM32'; ./myenv/Scripts/Activate; python Nap_Chute.py}"