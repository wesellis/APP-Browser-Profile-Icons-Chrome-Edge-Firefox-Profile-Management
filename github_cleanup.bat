@echo off
echo ========================================
echo  ProfilePop - Final Cleanup for GitHub
echo ========================================
echo.

cd /d "%~dp0"

echo Cleaning ProfilePop directory for GitHub release...
echo.

REM Remove all build artifacts
echo Removing build artifacts...
if exist "build" (
    rmdir /s /q "build"
    echo ✓ Removed build\ folder
)
if exist "dist" (
    rmdir /s /q "dist"
    echo ✓ Removed dist\ folder
)
if exist "ProfilePop.spec" (
    del "ProfilePop.spec"
    echo ✓ Removed ProfilePop.spec
)
if exist "app_icon.ico" (
    del "app_icon.ico"
    echo ✓ Removed app_icon.ico
)

REM Handle executables - move to releases folder
echo.
echo Handling executable files...
if not exist "releases" mkdir "releases"

if exist "ProfilePop.exe" (
    move "ProfilePop.exe" "releases\ProfilePop.exe" >nul
    echo ✓ Moved ProfilePop.exe to releases\ folder
)

REM Look for any versioned executables
for %%f in (ProfilePop-v*.exe) do (
    if exist "%%f" (
        move "%%f" "releases\%%f" >nul
        echo ✓ Moved %%f to releases\ folder
    )
)

REM Remove old cleanup scripts (keep only this one)
if exist "cleanup.bat" (
    del "cleanup.bat"
    echo ✓ Removed old cleanup.bat
)
if exist "final_cleanup.bat" (
    del "final_cleanup.bat"
    echo ✓ Removed old final_cleanup.bat
)

echo.
echo ========================================
echo  REPOSITORY STATUS
echo ========================================
echo.
echo ✅ Files ready for GitHub commit:
echo   - ProfilePop.py (main application)
echo   - ProfilePop.vbs (silent launcher)
echo   - ProfilePop_ICON.png (custom app icon)
echo   - logos\ (browser logo files)
echo   - build.bat and build_exe.py (build scripts)
echo   - README.md, LICENSE, requirements.txt
echo   - .gitignore (properly configured)
echo.
echo 📦 Release files (do NOT commit these):
if exist "releases" (
    echo   Files in releases\ folder:
    dir /b "releases\*.exe" 2>nul
    if errorlevel 1 (
        echo   - No executable files found
        echo   - Run build.bat to create ProfilePop executable
    )
) else (
    echo   - No releases\ folder found
    echo   - Run build.bat to create ProfilePop executable
)
echo.
echo ❌ Cleaned up (removed):
echo   - Build artifacts (build\, dist\, *.spec)  
echo   - Temporary files (app_icon.ico)
echo   - Old cleanup scripts
echo.
echo ========================================
echo  NEXT STEPS FOR GITHUB
echo ========================================
echo.
echo 1. BUILD EXECUTABLE (if needed):
echo    build.bat
echo.
echo 2. COMMIT TO GITHUB:
echo    - Commit all files EXCEPT releases\ folder
echo    - The .gitignore will handle excluding executables
echo.
echo 3. CREATE GITHUB RELEASE:
echo    - Go to GitHub → Releases → Create Release
echo    - Tag: v1.2.0 (or current version)
echo    - Upload the .exe file from releases\ folder
echo.
echo 4. USERS DOWNLOAD:
echo    - Users download .exe from GitHub Releases
echo    - No Python installation needed for end users
echo.
echo Repository is now clean and ready! 🚀
echo.
pause
