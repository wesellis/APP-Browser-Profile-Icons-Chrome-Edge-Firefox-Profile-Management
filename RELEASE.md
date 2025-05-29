# Release Process for ProfilePop

## 📦 Creating a New Release

### 1. Prepare the Code
```bash
# Update version info in ProfilePop.py if needed
# Test all functionality
# Update README.md if there are new features
```

### 2. Build the Executable
```bash
# Clean and build
cleanup.bat
build.bat
```

### 3. GitHub Release Steps
1. **Go to GitHub repository**
2. **Click "Releases" → "Create a new release"**
3. **Tag version**: `v1.0.0` (follow semantic versioning)
4. **Release title**: `ProfilePop v1.0.0 - Browser Profile Icon Generator`
5. **Upload `releases/ProfilePop.exe`** as an asset
6. **Write release notes** (see template below)

### 4. Release Notes Template
```markdown
## 🎉 ProfilePop v1.0.0

### ✨ New Features
- Multi-browser support (Edge, Firefox, Chrome)
- Custom colored backgrounds with 48-color palette
- Smart text contrast (white/black based on background)
- Professional rounded corner design
- Taskbar-optimized icon sizes

### 📦 Download
- **Windows Users**: Download `ProfilePop.exe` below - no installation needed!
- **Developers**: Clone the repository and run from source

### 🔧 System Requirements
- Windows 10/11 (Windows 7/8 may work)
- Browser profiles set up in Edge, Firefox, or Chrome

### 🐛 Bug Fixes
- Fixed taskbar icon sizing issues
- Resolved OneDrive sync conflicts with timestamped filenames
- Improved error handling for missing browsers

### 📝 Notes
- First stable release
- Portable executable includes all dependencies
- Source code available for customization
```

## 🏷️ Version Numbering
- **Major.Minor.Patch** (e.g., 1.0.0)
- **Major**: Breaking changes or major new features
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes, small improvements

## 📂 What Goes Where
- **GitHub Repository**: Source code, documentation, build scripts
- **GitHub Releases**: Executable files, release notes, version tags
- **Never commit**: .exe files, build artifacts, user-generated icons

## 🎯 Release Checklist
- [ ] Code tested and working
- [ ] Version number updated (if applicable)
- [ ] README.md reflects current features
- [ ] Clean build with `cleanup.bat` and `build.bat`
- [ ] GitHub release created with proper tag
- [ ] Executable uploaded as release asset
- [ ] Release notes written and published
