# 🚀 Browser Profile Icons - Installation Guide

## Overview

Browser Profile Icons is available in two formats:
1. **Chrome Extension** - For managing Chrome browser profiles (FREE with Pro upgrade)
2. **Desktop Application** - For Edge, Firefox, and Chrome profile icon customization

---

## 🌐 Chrome Extension Installation

### From Chrome Web Store (Recommended)
1. Visit the [Chrome Web Store listing](https://chrome.google.com/webstore/detail/browser-profile-icons-pro)
2. Click **"Add to Chrome"**
3. Confirm permissions when prompted
4. The extension icon will appear in your toolbar
5. Click the icon to start creating profiles!

### Manual Installation (For Developers)
1. Download the source code from GitHub
2. Open Chrome and navigate to `chrome://extensions/`
3. Enable **"Developer mode"** (toggle in top right)
4. Click **"Load unpacked"**
5. Select the `chrome-extension` folder
6. The extension will be installed locally

### First-Time Setup
1. Click the extension icon in your toolbar
2. You'll see the welcome screen with a 7-day Pro trial offer
3. Create your first profile:
   - Choose a name (e.g., "Work", "Personal")
   - Select a color theme
   - Optionally add a custom icon
4. Start switching between profiles instantly!

---

## 💻 Desktop Application Installation

### Windows Users (ProfilePop.exe)

#### Quick Install
1. Download `ProfilePop.exe` from the [latest release](https://github.com/wesellis/browser-profile-icons/releases)
2. Save to your preferred location (e.g., Desktop or Documents)
3. Double-click `ProfilePop.exe` to run
4. No installation required - it's portable!

#### Creating Desktop Shortcuts
1. Right-click `ProfilePop.exe`
2. Select **"Create shortcut"**
3. Move the shortcut to your Desktop
4. (Optional) Pin to Start Menu or Taskbar

#### First Run
- Windows Defender may show a warning (this is normal for unsigned apps)
- Click **"More info"** → **"Run anyway"**
- The app will open with the main interface

### Running from Source Code

#### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

#### Installation Steps
```bash
# Clone the repository
git clone https://github.com/wesellis/browser-profile-icons.git
cd browser-profile-icons

# Install dependencies
pip install -r requirements.txt

# Run the application
python ProfilePop.py
```

---

## 🔧 Configuration

### Chrome Extension Settings
1. Click the extension icon → **"Settings"** (gear icon)
2. Configure:
   - **Default profile**: Your main browsing profile
   - **Keyboard shortcuts**: Customize switching keys
   - **Auto-switch rules**: Set domains to specific profiles
   - **Cloud sync**: Enable to sync across devices (Pro)

### Desktop App Settings
- **Icon output folder**: Where generated icons are saved
- **Desktop shortcut location**: Where shortcuts are created
- **Color palette**: Customize available colors
- **Font settings**: Adjust text on icons

---

## 🆙 Upgrading to Pro

### Chrome Extension
1. Click the extension icon
2. Select **"Upgrade to Pro"**
3. Complete payment via Chrome Web Store ($4.99 one-time)
4. Pro features activate immediately

### Benefits of Pro
- ✅ Unlimited profiles (Free: 5 profiles)
- ✅ All keyboard shortcuts (Ctrl+Shift+1-9)
- ✅ Cloud sync across devices
- ✅ Custom icon uploads
- ✅ Auto-switching rules
- ✅ Import/Export profiles
- ✅ Priority support
- ✅ Lifetime updates

---

## 🔄 Updates

### Chrome Extension
- Updates automatically via Chrome Web Store
- Check for updates: `chrome://extensions/` → Enable developer mode → **"Update"**

### Desktop Application
- Download the latest version from [GitHub Releases](https://github.com/wesellis/browser-profile-icons/releases)
- Replace your existing `ProfilePop.exe` file

---

## 🛠️ Troubleshooting

### Chrome Extension Issues

| Problem | Solution |
|---------|----------|
| Extension not visible | Click puzzle icon in toolbar → Pin "Browser Profile Icons" |
| Profiles not switching | Ensure you have Chrome profiles created in `chrome://settings/manageProfile` |
| Keyboard shortcuts not working | Check for conflicts in `chrome://extensions/shortcuts` |
| Cloud sync not working | Sign in with Google account in extension settings |

### Desktop App Issues

| Problem | Solution |
|---------|----------|
| "Windows protected your PC" | Click "More info" → "Run anyway" (app is safe but unsigned) |
| Browser not detected | Ensure browser is installed in default location |
| Icons not appearing | Check output folder permissions |
| Fonts look wrong | Install Windows font smoothing |

---

## 🔒 Permissions Explained

### Chrome Extension Permissions
- **storage**: Save your profile settings locally
- **tabs**: Switch between browser profiles
- **identity**: Enable cloud sync with Google account (Pro)
- **management**: Detect installed extensions for compatibility

All permissions are used solely for core functionality. No data is collected or shared.

---

## 🆘 Support

### Getting Help
- **Documentation**: [GitHub Wiki](https://github.com/wesellis/browser-profile-icons/wiki)
- **Bug Reports**: [GitHub Issues](https://github.com/wesellis/browser-profile-icons/issues)
- **Email Support**: support@browserprofileicons.com
- **Pro Support**: Priority response within 24 hours

### Community
- Star the project on [GitHub](https://github.com/wesellis/browser-profile-icons)
- Share feedback and feature requests
- Contribute to development

---

## 🎉 Next Steps

1. **Create your profiles** - Organize work, personal, and project browsing
2. **Set up shortcuts** - Use keyboard shortcuts for instant switching
3. **Customize appearance** - Make each profile visually distinct
4. **Enable cloud sync** (Pro) - Access profiles on all your devices
5. **Share with colleagues** - Help others stay organized!

---

*Thank you for choosing Browser Profile Icons! We're committed to making your browsing experience more organized and efficient.*