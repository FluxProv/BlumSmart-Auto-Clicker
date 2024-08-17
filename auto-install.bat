@echo off
chcp 65001
cls
:: Устанавливаем цвет консоли (синий для заголовков, белый для текста)
color 1F

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
    echo Python не найден. Загружаем и устанавливаем Python...

    :: Задание версии Python и URL для скачивания
    set "PYTHON_VERSION=3.9.7"
    set "PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe"
    set "PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_INSTALLER%"

    :: Скачивание установщика Python
    powershell -Command "Invoke-WebRequest -Uri %PYTHON_URL% -OutFile %PYTHON_INSTALLER%"

    :: Установка Python тихо
    start /wait "" %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1

    :: Удаление установщика
    del %PYTHON_INSTALLER%

    echo Установка Python завершена.
) ELSE (
    echo Python уже установлен.
)

:: Обновление pip
echo Обновление pip...
python -m pip install --upgrade pip

:: Создание requirements.txt
echo Создание файла requirements.txt...
(
echo PyQt5
echo requests
) > requirements.txt

:: Установка библиотек из requirements.txt
echo Установка библиотек из requirements.txt...
pip install -r requirements.txt

:: Удаление файла requirements.txt
echo Удаление файла requirements.txt...
del requirements.txt

:: Компиляция скрипта в EXE
echo -------------------------
echo Компиляция скрипта в EXE...
pyinstaller --onefile --noconsole --icon=Source-Code/images/icon.ico --name=BlumClicker Source-Code/interface.py

:: Перемещение файлов и папок
echo Перемещение файлов и папок...
if not exist "Files\compile" mkdir "Files\compile"
move /Y dist\BlumClicker.exe Files\compile\
move /Y Source-Code\images Files\compile\
rmdir /s /q dist

:: Проверка существования иконки
if not exist "%CD%\Files\compile\images\icon.ico" (
    echo Иконка не найдена: "%CD%\Files\compile\images\icon.ico"
    echo Убедитесь, что иконка присутствует в указанной папке.
    exit /b 1
)

:: Создание ярлыка на рабочем столе
echo Создание ярлыка на рабочем столе...
set "desktopShortcut=%USERPROFILE%\Desktop\BlumClicker.lnk"
set "targetPath=%CD%\Files\compile\BlumClicker.exe"
set "iconPath=%CD%\Files\compile\images\icon.ico"

powershell -Command ^
    "$ws = New-Object -ComObject WScript.Shell; ^
    $s = $ws.CreateShortcut('%desktopShortcut%'); ^
    $s.TargetPath = '%targetPath%'; ^
    $s.IconLocation = '%iconPath%'; ^
    $s.Save()"

:: Сообщение о завершении установки
echo -------------------------
echo Установка завершена! Ярлык создан на рабочем столе.
timeout /t 5 >nul

:: Удаление самого BAT файла
echo Удаление BAT файла...
del "%~f0"
