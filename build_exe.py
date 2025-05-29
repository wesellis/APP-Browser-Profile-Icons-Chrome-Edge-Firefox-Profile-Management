# build_exe.py - Script to build ProfilePop into a portable exe with version
import subprocess
import sys
import os
import shutil

def get_version():
    """Extract version from ProfilePop.py"""
    try:
        with open('ProfilePop.py', 'r') as f:
            for line in f:
                if '__version__' in line and '=' in line:
                    return line.split('"')[1]
        return "1.0.0"  # fallback
    except:
        return "1.0.0"

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    print("Installing PyInstaller...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
        print("✅ PyInstaller installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install PyInstaller: {e}")
        return False

def build_exe():
    """Build the executable using PyInstaller"""
    version = get_version()
    print(f"Building ProfilePop v{version}...")
    
    # Check for custom icon and convert if needed
    icon_arg = None
    if os.path.exists('ProfilePop_ICON.png'):
        print("Converting PNG icon to ICO format...")
        try:
            from PIL import Image
            img = Image.open('ProfilePop_ICON.png')
            img.save('app_icon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
            if os.path.exists('app_icon.ico'):
                icon_arg = '--icon=app_icon.ico'
                print("✅ Icon converted successfully")
            else:
                print("⚠️ Icon conversion failed")
        except Exception as e:
            print(f"⚠️ Icon conversion error: {e}")
    else:
        print("ℹ️ No ProfilePop_ICON.png found, building without custom icon")
    
    # PyInstaller command with version in name
    exe_name = f"ProfilePop-v{version}"
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',                    # Single executable file
        '--windowed',                   # No console window
        f'--name={exe_name}',           # Output name with version
        '--add-data=logos;logos',       # Include logos folder
        '--hidden-import=PIL._tkinter_finder',  # Fix PIL import issues
        '--hidden-import=PIL.Image',
        '--hidden-import=PIL.ImageDraw', 
        '--hidden-import=PIL.ImageFont',
        '--hidden-import=winshell',
        '--hidden-import=win32com.client',
        'ProfilePop.py'
    ]
    
    # Add icon if available
    if icon_arg:
        cmd.insert(-1, icon_arg)
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Build completed successfully!")
        
        # Check if exe was created
        exe_path = os.path.join('dist', f'{exe_name}.exe')
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"📦 {exe_name}.exe created: {size_mb:.1f} MB")
            print(f"📁 Location: {os.path.abspath(exe_path)}")
            
            # Copy to current directory for convenience
            shutil.copy2(exe_path, f'{exe_name}.exe')
            print(f"📋 Copied to current directory: {exe_name}.exe")
            
            return True
        else:
            print("❌ Executable not found in dist folder")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

def cleanup():
    """Clean up build files"""
    print("Cleaning up build files...")
    
    folders_to_remove = ['build', 'dist', '__pycache__']
    files_to_remove = ['ProfilePop.spec', 'app_icon.ico']
    
    for folder in folders_to_remove:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"🗑️ Removed {folder}")
    
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑️ Removed {file}")

def main():
    version = get_version()
    print("🚀 ProfilePop Portable EXE Builder")
    print("=" * 40)
    print(f"Version: {version}")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists('ProfilePop.py'):
        print("❌ ProfilePop.py not found. Run this script in the ProfilePop directory.")
        return
    
    if not os.path.exists('logos'):
        print("❌ logos folder not found. Make sure the logos folder exists.")
        return
    
    # Install PyInstaller
    if not install_pyinstaller():
        return
    
    # Build the executable
    if build_exe():
        version = get_version()
        print(f"\n🎉 SUCCESS!")
        print(f"Your portable ProfilePop-v{version}.exe is ready!")
        print("\nTo distribute:")
        print(f"1. Copy ProfilePop-v{version}.exe to any Windows computer")
        print("2. Double-click to run - no installation needed!")
        print("3. The logos are embedded in the exe")
        
        # Ask about cleanup
        choice = input("\nClean up build files? (y/n): ").lower().strip()
        if choice in ['y', 'yes']:
            cleanup()
    else:
        print("\n❌ Build failed. Check error messages above.")

if __name__ == "__main__":
    main()
