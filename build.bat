@echo off
echo ========================================
echo  ProfilePop Portable EXE Builder
echo ========================================
echo.

cd /d "%~dp0"

REM Check if ProfilePop.py exists
if not exist "ProfilePop.py" (
    echo ERROR: ProfilePop.py not found
    echo Make sure you're running this in the ProfilePop directory
    pause
    exit /b 1
)

REM Check if logos folder exists
if not exist "logos" (
    echo ERROR: logos folder not found
    echo Make sure the logos folder exists in this directory
    pause
    exit /b 1
)

echo Installing PyInstaller...
pip install pyinstaller --quiet
if %errorlevel% neq 0 (
    echo ERROR: Failed to install PyInstaller
    echo Make sure Python and pip are installed
    pause
    exit /b 1
)

REM Extract version from ProfilePop.py
for /f "tokens=3 delims=\"" %%a in ('findstr "__version__" ProfilePop.py') do set VERSION=%%a
echo Building ProfilePop v%VERSION%...
echo This may take a few minutes...

REM Check if icon exists and convert if needed
if exist "ProfilePop_ICON.png" (
    echo Converting PNG icon to ICO format...
    python -c "from PIL import Image; img = Image.open('ProfilePop_ICON.png'); img.save('app_icon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])"
    if exist "app_icon.ico" (
        echo Icon converted successfully
        python -m PyInstaller --onefile --windowed --name=ProfilePop-v%VERSION% --icon=app_icon.ico --add-data="logos;logos" --hidden-import=PIL._tkinter_finder --hidden-import=PIL.Image --hidden-import=PIL.ImageDraw --hidden-import=PIL.ImageFont --hidden-import=winshell --hidden-import=win32com.client ProfilePop.py
    ) else (
        echo Icon conversion failed, building without custom icon
        python -m PyInstaller --onefile --windowed --name=ProfilePop-v%VERSION% --add-data="logos;logos" --hidden-import=PIL._tkinter_finder --hidden-import=PIL.Image --hidden-import=PIL.ImageDraw --hidden-import=PIL.ImageFont --hidden-import=winshell --hidden-import=win32com.client ProfilePop.py
    )
) else (
    echo No ProfilePop_ICON.png found, building without custom icon
    python -m PyInstaller --onefile --windowed --name=ProfilePop-v%VERSION% --add-data="logos;logos" --hidden-import=PIL._tkinter_finder --hidden-import=PIL.Image --hidden-import=PIL.ImageDraw --hidden-import=PIL.ImageFont --hidden-import=winshell --hidden-import=win32com.client ProfilePop.py
)

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Build failed
    pause
    exit /b 1
)

REM Check if exe was created with version number
for /f "tokens=3 delims=\"" %%a in ('findstr "__version__" ProfilePop.py') do set VERSION=%%a
if exist "dist\ProfilePop-v%VERSION%.exe" (
    echo.
    echo SUCCESS! ProfilePop-v%VERSION%.exe created
    copy "dist\ProfilePop-v%VERSION%.exe" "ProfilePop-v%VERSION%.exe" >nul
    echo Copied to: ProfilePop-v%VERSION%.exe
    
    echo.
    echo File size:
    dir "ProfilePop-v%VERSION%.exe" | find "ProfilePop-v%VERSION%.exe"
    
    echo.
    echo Your versioned ProfilePop-v%VERSION%.exe is ready!
    echo You can copy this file to any Windows computer and run it.
    echo.
    
    set /p cleanup="Clean up build files? (y/n): "
    if /i "%cleanup%"=="y" (
        rmdir /s /q build 2>nul
        rmdir /s /q dist 2>nul
        del ProfilePop.spec 2>nul
        echo Build files cleaned up
    )
) else (
    echo ERROR: ProfilePop.exe not found in dist folder
    pause
    exit /b 1
)

echo.
echo Done! Press any key to exit...
pause >nul
