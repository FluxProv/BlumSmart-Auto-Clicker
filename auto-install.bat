@echo off
echo.
echo ███████╗██╗░░░░░██╗░░░██╗██╗░░██╗
echo ██╔════╝██║░░░░░██║░░░██║╚██╗██╔╝
echo █████╗░░██║░░░░░██║░░░██║░╚███╔╝░
echo ██╔══╝░░██║░░░░░██║░░░██║░██╔██╗░
echo ██║░░░░░███████╗╚██████╔╝██╔╝╚██╗
echo ╚═╝░░░░░╚══════╝░╚═════╝░╚═╝░░╚═╝
echo.

:: Проверка наличия Python
echo Проверка наличия Python...
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python не найден. Пожалуйста, установите Python.
    exit /b 1
)

:: Создание requirements.txt
echo Создание файла requirements.txt...
pip freeze > requirements.txt

:: Установка зависимостей
echo Установка зависимостей...
pip install -r requirements.txt

:: Компиляция скрипта в EXE
echo Компиляция скрипта в EXE...
pyinstaller --onefile --noconsole --icon=Source-Code/images/icon.ico --name=BlumClicker Source-Code/interface.py

:: Перемещение файлов и папок
echo Перемещение файлов и папок...
if not exist "Files\compile" mkdir "Files\compile"
move /Y dist\BlumClicker.exe Files\compile\
move /Y Source-Code\images Files\compile\
rmdir /s /q dist

:: Сообщение о завершении установки
echo -------------------------
echo Установка завершена!
pause
