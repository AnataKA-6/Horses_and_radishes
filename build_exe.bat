@echo off
title Сборка игры "Лошади и Редиски"
echo ========================================
echo   СБОРКА ИГРЫ "ЛОШАДИ И РЕДИСКИ"
echo ========================================
echo.

:: Проверка установки PyInstaller
py -m pip show pyinstaller > nul 2>&1
if errorlevel 1 (
    echo Установка PyInstaller...
    py -m pip install pyinstaller
    echo.
)

:: Проверка наличия иконки
if not exist "icon.ico" (
    echo ВНИМАНИЕ: Файл icon.ico не найден!
    set ICON_OPTION=
) else (
    echo ? Найден icon.ico
    set ICON_OPTION=--icon=icon.ico
)

:: Очистка
echo.
echo Очистка старых файлов...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.spec" del /q *.spec
echo.

:: Сборка EXE
echo Сборка EXE файла...
echo.

:: ? ИКОНКА ДОБАВЛЯЕТСЯ ДВУМЯ СПОСОБАМИ
py -m PyInstaller --onefile ^
    --windowed ^
    %ICON_OPTION% ^
    --name "Лошади и Редиски" ^
    --add-data "sounds;sounds" ^
    --add-data "horse_images;horse_images" ^
    --add-data "gif;gif" ^
    --add-data "icon.ico;." ^
    --hidden-import=PIL ^
    --hidden-import=PIL.Image ^
    --hidden-import=PIL.ImageDraw ^
    --hidden-import=PIL.ImageSequence ^
    --hidden-import=PIL.ImageTk ^
    --hidden-import=pygame ^
    --hidden-import=pygame.mixer ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.ttk ^
    --hidden-import=pathlib ^
    --hidden-import=json ^
    --hidden-import=random ^
    --hidden-import=datetime ^
    --hidden-import=os ^
    --hidden-import=sys ^
    --hidden-import=math ^
    --hidden-import=shutil ^
    --collect-all PIL ^
    --collect-all pygame ^
    horse_board_game.py

if errorlevel 1 (
    echo.
    echo ? ОШИБКА при сборке!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ? ГОТОВО!
echo ========================================
echo.
echo EXE файл создан: dist\Лошади и Редиски.exe
echo.
pause