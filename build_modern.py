#!/usr/bin/env python3
"""
Modern build script for ProfilePop
Creates optimized executables for Windows, macOS, and Linux
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import json
import platform

class ModernBuilder:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.build_dir = self.root_dir / "build"
        self.dist_dir = self.root_dir / "dist"
        self.release_dir = self.root_dir / "releases"
        self.platform = platform.system().lower()
        
    def clean(self):
        """Clean previous build artifacts"""
        print("🧹 Cleaning previous builds...")
        for dir_path in [self.build_dir, self.dist_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
        print("✅ Clean complete")
    
    def prepare_assets(self):
        """Prepare assets for building"""
        print("📦 Preparing assets...")
        
        # Ensure icon exists
        if not (self.root_dir / "ProfilePop_ICON.ico").exists():
            self.create_icon()
        
        # Create version file
        self.create_version_file()
        
        print("✅ Assets prepared")
    
    def create_icon(self):
        """Create ICO file from PNG"""
        png_path = self.root_dir / "ProfilePop_ICON.png"
        ico_path = self.root_dir / "ProfilePop_ICON.ico"
        
        if png_path.exists():
            try:
                from PIL import Image
                img = Image.open(png_path)
                img.save(ico_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (128, 128), (256, 256)])
                print("✅ Icon created")
            except Exception as e:
                print(f"⚠️ Could not create icon: {e}")
    
    def create_version_file(self):
        """Create version info file for Windows"""
        if self.platform != "windows":
            return
        
        version_info = '''
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(3, 0, 0, 0),
    prodvers=(3, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Wesley Ellis'),
        StringStruct(u'FileDescription', u'Browser Profile Icon Generator'),
        StringStruct(u'FileVersion', u'3.0.0.0'),
        StringStruct(u'InternalName', u'ProfilePop'),
        StringStruct(u'LegalCopyright', u'© 2025 Wesley Ellis'),
        StringStruct(u'OriginalFilename', u'ProfilePop.exe'),
        StringStruct(u'ProductName', u'ProfilePop Modern'),
        StringStruct(u'ProductVersion', u'3.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
        with open(self.root_dir / "version.txt", "w") as f:
            f.write(version_info)
    
    def build_executable(self):
        """Build executable for current platform"""
        print(f"🔨 Building for {self.platform.title()}...")
        
        # PyInstaller spec file
        spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['ProfilePop_Modern.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('logos/*.png', 'logos'),
        ('ProfilePop_ICON.ico', '.'),
        ('chrome-extension', 'chrome-extension'),
    ],
    hiddenimports=[
        'customtkinter',
        'PIL._tkinter_finder',
        'darkdetect',
        'tkinterdnd2',
        'aiofiles',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'pytest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ProfilePop',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='ProfilePop_ICON.ico',
    version='version.txt' if sys.platform == 'win32' else None,
)

# macOS specific
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='ProfilePop.app',
        icon='ProfilePop_ICON.icns',
        bundle_identifier='com.wesellis.profilepop',
        info_plist={{
            'CFBundleName': 'ProfilePop',
            'CFBundleDisplayName': 'ProfilePop Modern',
            'CFBundleVersion': '3.0.0',
            'CFBundleShortVersionString': '3.0.0',
            'NSHighResolutionCapable': True,
            'NSRequiresAquaSystemAppearance': False,
        }},
    )
'''
        
        # Write spec file
        spec_path = self.root_dir / "ProfilePop.spec"
        with open(spec_path, "w") as f:
            f.write(spec_content)
        
        # Run PyInstaller
        try:
            subprocess.run([
                sys.executable, "-m", "PyInstaller",
                "--clean",
                "--noconfirm",
                str(spec_path)
            ], check=True)
            
            print("✅ Build complete")
            self.move_to_releases()
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Build failed: {e}")
            sys.exit(1)
    
    def move_to_releases(self):
        """Move built executable to releases folder"""
        print("📁 Moving to releases...")
        
        self.release_dir.mkdir(exist_ok=True)
        
        if self.platform == "windows":
            src = self.dist_dir / "ProfilePop.exe"
            dst = self.release_dir / "ProfilePop_Windows.exe"
        elif self.platform == "darwin":
            src = self.dist_dir / "ProfilePop.app"
            dst = self.release_dir / "ProfilePop_macOS.app"
            shutil.copytree(src, dst, dirs_exist_ok=True)
            return
        else:  # Linux
            src = self.dist_dir / "ProfilePop"
            dst = self.release_dir / "ProfilePop_Linux"
        
        if src.exists():
            shutil.copy2(src, dst)
            print(f"✅ Executable moved to {dst}")
    
    def create_portable_package(self):
        """Create portable package with all files"""
        print("📦 Creating portable package...")
        
        package_dir = self.release_dir / f"ProfilePop_Portable_{self.platform}"
        package_dir.mkdir(exist_ok=True)
        
        # Copy executable
        if self.platform == "windows":
            shutil.copy2(self.release_dir / "ProfilePop_Windows.exe", package_dir / "ProfilePop.exe")
        elif self.platform == "darwin":
            shutil.copytree(self.release_dir / "ProfilePop_macOS.app", package_dir / "ProfilePop.app", dirs_exist_ok=True)
        else:
            shutil.copy2(self.release_dir / "ProfilePop_Linux", package_dir / "ProfilePop")
        
        # Copy supporting files
        files_to_copy = [
            "README.md",
            "LICENSE",
            "INSTALLATION_GUIDE.md",
            "requirements.txt"
        ]
        
        for file in files_to_copy:
            src = self.root_dir / file
            if src.exists():
                shutil.copy2(src, package_dir)
        
        # Copy logos
        logos_dir = package_dir / "logos"
        logos_dir.mkdir(exist_ok=True)
        shutil.copytree(self.root_dir / "logos", logos_dir, dirs_exist_ok=True)
        
        # Create ZIP archive
        archive_name = f"ProfilePop_v3.0.0_{self.platform}"
        shutil.make_archive(
            self.release_dir / archive_name,
            'zip',
            package_dir
        )
        
        print(f"✅ Portable package created: {archive_name}.zip")
    
    def build_chrome_extension(self):
        """Package Chrome extension"""
        print("🌐 Building Chrome extension...")
        
        ext_dir = self.root_dir / "chrome-extension"
        ext_dist = self.release_dir / "chrome-extension"
        
        # Copy extension files
        shutil.copytree(ext_dir, ext_dist, dirs_exist_ok=True)
        
        # Update manifest version
        manifest_path = ext_dist / "manifest.json"
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        manifest['version'] = '3.0.0'
        
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        # Create ZIP for Chrome Web Store
        shutil.make_archive(
            self.release_dir / "ProfilePop_ChromeExtension_v3.0.0",
            'zip',
            ext_dist
        )
        
        print("✅ Chrome extension packaged")
    
    def run_tests(self):
        """Run tests before building"""
        print("🧪 Running tests...")
        
        try:
            subprocess.run([sys.executable, "-m", "pytest", "tests/"], check=True)
            print("✅ All tests passed")
        except subprocess.CalledProcessError:
            print("⚠️ Some tests failed, continuing anyway...")
        except FileNotFoundError:
            print("⚠️ No tests found, skipping...")
    
    def build_all(self):
        """Run complete build process"""
        print("🚀 ProfilePop Modern Builder v3.0")
        print("=" * 50)
        
        self.clean()
        self.prepare_assets()
        # self.run_tests()  # Uncomment when tests are ready
        self.build_executable()
        self.create_portable_package()
        self.build_chrome_extension()
        
        print("\n" + "=" * 50)
        print("🎉 Build complete!")
        print(f"📁 Check the 'releases' folder for output files")

def main():
    """Main entry point"""
    builder = ModernBuilder()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "clean":
            builder.clean()
        elif command == "test":
            builder.run_tests()
        elif command == "chrome":
            builder.build_chrome_extension()
        else:
            print(f"Unknown command: {command}")
    else:
        builder.build_all()

if __name__ == "__main__":
    main()