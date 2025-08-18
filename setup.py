#!/usr/bin/env python3
"""
Setup script for ProfilePop Modern
Handles installation, dependencies, and initial configuration
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import json
import shutil

class ProfilePopSetup:
    def __init__(self):
        self.platform = platform.system().lower()
        self.python_version = sys.version_info
        self.root_dir = Path(__file__).parent
        
    def check_python_version(self):
        """Check if Python version meets requirements"""
        if self.python_version < (3, 8):
            print("❌ Python 3.8 or higher is required")
            print(f"   Current version: {sys.version}")
            return False
        print(f"✅ Python {self.python_version.major}.{self.python_version.minor} detected")
        return True
    
    def install_dependencies(self):
        """Install required Python packages"""
        print("\n📦 Installing dependencies...")
        
        # Upgrade pip first
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=False)
        
        # Install requirements
        requirements_file = self.root_dir / "requirements.txt"
        if requirements_file.exists():
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ All dependencies installed successfully")
                return True
            else:
                print("⚠️ Some dependencies failed to install")
                print(result.stderr)
                return False
        else:
            print("❌ requirements.txt not found")
            return False
    
    def setup_desktop_app(self):
        """Setup desktop application"""
        print("\n🖥️ Setting up desktop application...")
        
        # Create desktop shortcut (Windows)
        if self.platform == "windows":
            self.create_windows_shortcut()
        elif self.platform == "darwin":
            self.create_macos_app()
        elif self.platform == "linux":
            self.create_linux_desktop_file()
        
        print("✅ Desktop application ready")
    
    def create_windows_shortcut(self):
        """Create Windows desktop shortcut"""
        try:
            import win32com.client
            
            desktop = Path.home() / "Desktop"
            shortcut_path = desktop / "ProfilePop Modern.lnk"
            
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(shortcut_path))
            
            # Set shortcut properties
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = str(self.root_dir / "ProfilePop_Modern.py")
            shortcut.WorkingDirectory = str(self.root_dir)
            shortcut.IconLocation = str(self.root_dir / "ProfilePop_ICON.ico")
            shortcut.Description = "Browser Profile Icon Generator"
            
            shortcut.save()
            print(f"✅ Desktop shortcut created: {shortcut_path}")
            
        except ImportError:
            print("⚠️ pywin32 not installed - skipping shortcut creation")
        except Exception as e:
            print(f"⚠️ Could not create shortcut: {e}")
    
    def create_macos_app(self):
        """Create macOS application bundle"""
        app_name = "ProfilePop Modern.app"
        app_path = Path("/Applications") / app_name
        
        # Create app structure
        contents_dir = app_path / "Contents"
        macos_dir = contents_dir / "MacOS"
        resources_dir = contents_dir / "Resources"
        
        # Create directories
        for dir_path in [contents_dir, macos_dir, resources_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create launcher script
        launcher_script = macos_dir / "ProfilePop"
        launcher_content = f"""#!/bin/bash
cd "{self.root_dir}"
{sys.executable} ProfilePop_Modern.py
"""
        launcher_script.write_text(launcher_content)
        launcher_script.chmod(0o755)
        
        # Create Info.plist
        info_plist = contents_dir / "Info.plist"
        plist_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>ProfilePop Modern</string>
    <key>CFBundleDisplayName</key>
    <string>ProfilePop Modern</string>
    <key>CFBundleIdentifier</key>
    <string>com.wesellis.profilepop</string>
    <key>CFBundleVersion</key>
    <string>3.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleExecutable</key>
    <string>ProfilePop</string>
</dict>
</plist>"""
        info_plist.write_text(plist_content)
        
        print(f"✅ macOS app created: {app_path}")
    
    def create_linux_desktop_file(self):
        """Create Linux desktop file"""
        desktop_file_path = Path.home() / ".local/share/applications/profilepop.desktop"
        desktop_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        desktop_content = f"""[Desktop Entry]
Name=ProfilePop Modern
Comment=Browser Profile Icon Generator
Exec={sys.executable} {self.root_dir}/ProfilePop_Modern.py
Icon={self.root_dir}/ProfilePop_ICON.png
Terminal=false
Type=Application
Categories=Utility;Graphics;
"""
        
        desktop_file_path.write_text(desktop_content)
        desktop_file_path.chmod(0o755)
        
        print(f"✅ Desktop file created: {desktop_file_path}")
    
    def setup_chrome_extension(self):
        """Setup Chrome extension for development"""
        print("\n🌐 Setting up Chrome extension...")
        
        ext_dir = self.root_dir / "chrome-extension"
        
        if not ext_dir.exists():
            print("❌ Chrome extension directory not found")
            return False
        
        # Check manifest
        manifest_file = ext_dir / "manifest.json"
        if manifest_file.exists():
            with open(manifest_file, 'r') as f:
                manifest = json.load(f)
            
            print(f"✅ Chrome Extension v{manifest.get('version', 'Unknown')} ready")
            print("\n📝 To install the extension:")
            print("   1. Open Chrome and go to chrome://extensions/")
            print("   2. Enable 'Developer mode'")
            print(f"   3. Click 'Load unpacked' and select: {ext_dir}")
            return True
        else:
            print("❌ manifest.json not found")
            return False
    
    def create_config(self):
        """Create initial configuration file"""
        config_file = self.root_dir / "config.json"
        
        if not config_file.exists():
            config = {
                "version": "3.0.0",
                "theme": "dark",
                "auto_save": True,
                "check_updates": True,
                "default_browser": "chrome",
                "default_shape": "rounded",
                "default_color": "#3388de"
            }
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            print("✅ Configuration file created")
    
    def download_browser_logos(self):
        """Ensure browser logos are present"""
        logos_dir = self.root_dir / "logos"
        logos_dir.mkdir(exist_ok=True)
        
        required_logos = [
            "google-chrome-logo-main-icon.png",
            "microsoft-edge-browser-logo-blue-green-gradient-icon.png",
            "firefox-browser-logo-red-yellow-blue-circle-icon.png"
        ]
        
        missing_logos = []
        for logo in required_logos:
            if not (logos_dir / logo).exists():
                missing_logos.append(logo)
        
        if missing_logos:
            print(f"⚠️ Missing logos: {', '.join(missing_logos)}")
            print("   Please download browser logos to the 'logos' directory")
        else:
            print("✅ All browser logos present")
    
    def test_installation(self):
        """Test if installation was successful"""
        print("\n🧪 Testing installation...")
        
        try:
            # Test imports
            import customtkinter
            import PIL
            import aiofiles
            
            print("✅ All required modules can be imported")
            
            # Test if app can be launched
            app_file = self.root_dir / "ProfilePop_Modern.py"
            if app_file.exists():
                print("✅ Application file found")
                return True
            else:
                print("❌ Application file not found")
                return False
                
        except ImportError as e:
            print(f"❌ Import error: {e}")
            return False
    
    def run_setup(self):
        """Run complete setup process"""
        print("🚀 ProfilePop Modern Setup v3.0")
        print("=" * 50)
        
        # Check Python version
        if not self.check_python_version():
            sys.exit(1)
        
        # Install dependencies
        if not self.install_dependencies():
            print("\n⚠️ Setup completed with warnings")
            print("   Some dependencies may need manual installation")
        
        # Setup desktop app
        self.setup_desktop_app()
        
        # Setup Chrome extension
        self.setup_chrome_extension()
        
        # Create config
        self.create_config()
        
        # Check logos
        self.download_browser_logos()
        
        # Test installation
        if self.test_installation():
            print("\n" + "=" * 50)
            print("✅ Setup completed successfully!")
            print("\n🎉 ProfilePop Modern is ready to use!")
            print("\nTo start the application:")
            print(f"   python ProfilePop_Modern.py")
            
            if self.platform == "windows":
                print("\nOr use the desktop shortcut on your Desktop")
        else:
            print("\n⚠️ Setup completed with issues")
            print("   Please check the error messages above")
    
    def uninstall(self):
        """Uninstall ProfilePop"""
        print("🗑️ Uninstalling ProfilePop...")
        
        # Remove desktop shortcuts
        if self.platform == "windows":
            shortcut = Path.home() / "Desktop" / "ProfilePop Modern.lnk"
            if shortcut.exists():
                shortcut.unlink()
                print("✅ Desktop shortcut removed")
        
        elif self.platform == "darwin":
            app_path = Path("/Applications/ProfilePop Modern.app")
            if app_path.exists():
                shutil.rmtree(app_path)
                print("✅ Application removed")
        
        elif self.platform == "linux":
            desktop_file = Path.home() / ".local/share/applications/profilepop.desktop"
            if desktop_file.exists():
                desktop_file.unlink()
                print("✅ Desktop file removed")
        
        # Remove config
        config_file = self.root_dir / "config.json"
        if config_file.exists():
            config_file.unlink()
            print("✅ Configuration removed")
        
        print("\n✅ Uninstall complete")
        print("   Python packages were not removed (use pip uninstall if needed)")

def main():
    """Main entry point"""
    setup = ProfilePopSetup()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "uninstall":
            setup.uninstall()
        elif command == "test":
            setup.test_installation()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python setup.py [uninstall|test]")
    else:
        setup.run_setup()

if __name__ == "__main__":
    main()