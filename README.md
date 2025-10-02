# Browser Profile Icon Generator v3.0

A comprehensive tool for creating custom icons for browser profiles in Chrome, Edge, and Firefox.

[![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Stars](https://img.shields.io/github/stars/wesellis/APP-Browser-Profile-Icons-Chrome-Edge-Firefox-Profile-Management?style=flat-square)](https://github.com/wesellis/APP-Browser-Profile-Icons-Chrome-Edge-Firefox-Profile-Management/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/wesellis/APP-Browser-Profile-Icons-Chrome-Edge-Firefox-Profile-Management?style=flat-square)](https://github.com/wesellis/APP-Browser-Profile-Icons-Chrome-Edge-Firefox-Profile-Management/commits)
[![Completion](https://img.shields.io/badge/Completion-90%25-brightgreen?style=flat-square)](#project-status)

---

## Screenshot

![Browser Profile Icon Generator](docs/images/ProfilePop%20-%20Browser%20Profile%20Icon%20Generator%20-%20Main%20Window.png)

---

## What is This?

A comprehensive solution for managing browser profiles with custom icons. Includes both a desktop application and browser extensions for Chrome, Edge, and Firefox.

## Features

### Desktop Application (ProfilePop)
- **🎨 Icon Generation**: Create custom profile icons with text, colors, and shapes
- **🖌️ Multiple Shapes**: Circle, rounded, square, hexagon, badge styles
- **🎨 Rich Color Palette**: 20+ pre-defined colors with gradient support
- **✨ Visual Effects**: Shadows, glow, borders, and opacity controls
- **📁 Multi-Browser Support**: Chrome, Edge, Firefox, Brave, Opera, Vivaldi, Safari
- **🔧 Cross-Platform**: Windows, macOS, and Linux support
- **💾 Export/Import**: Save and restore profile configurations
- **📦 Icon Templates**: 26+ pre-designed templates for common use cases

### Browser Extensions

#### Chrome Extension (Manifest V3)
- ✅ Profile management and quick switching
- ✅ Keyboard shortcuts (Alt+P, Ctrl+Shift+1/2/3)
- ✅ Import/Export profiles
- ✅ Custom icons and colors
- ✅ Context menu integration
- ✅ Notifications

#### Firefox Extension (Manifest V2)
- ✅ Full Firefox compatibility
- ✅ Profile switching and management
- ✅ Keyboard shortcuts
- ✅ Export/Import functionality
- ✅ Settings page
- ✅ Welcome screen

#### Edge Extension (Manifest V3)
- ✅ Microsoft Edge compatibility
- ✅ Same features as Chrome extension
- ✅ Edge-specific optimizations

## What's New in v3.0

### Major Improvements
- 🎯 **Complete Firefox Support**: Full-featured Firefox extension
- 🚀 **Simplified Extensions**: Removed incomplete Pro features, focused on core functionality
- 📚 **Icon Template Library**: 26+ pre-designed templates across 10 categories
- 🌐 **Edge Support**: Dedicated Microsoft Edge extension
- ✅ **Test Suite**: Comprehensive pytest test coverage
- 🧹 **Code Cleanup**: Removed non-functional cloud sync and payment code

### Icon Template Categories
- Professional & Business (Work, Development, Admin, Testing, Freelance)
- Personal Use (Shopping, Travel, Health, Fitness, Food)
- Education & Learning (School, Research)
- Entertainment & Games (Gaming, Music, Video, Sports)
- Creative & Design (Photography, Design, Creative)
- Social Media
- Productivity & Tools
- News & Information

## Installation

### Desktop Application

```bash
# Clone the repository
git clone https://github.com/wesellis/browser-profile-icons.git
cd browser-profile-icons

# Install dependencies
pip install -r requirements.txt

# Run the application
python ProfilePop_Modern.py
```

### Browser Extensions

#### Chrome
1. Open Chrome and go to `chrome://extensions`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `chrome-extension` folder

#### Firefox
1. Open Firefox and go to `about:debugging#/runtime/this-firefox`
2. Click "Load Temporary Add-on"
3. Navigate to `firefox-extension` folder
4. Select `manifest.json`

#### Edge
1. Open Edge and go to `edge://extensions`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `edge-extension` folder

## Usage

### Desktop App: Creating Profile Icons

1. **Select Browser**: Choose your browser from the sidebar
2. **Customize**: Pick colors, shapes, and effects in the right panel
3. **Generate**: Click "Generate All Icons" to create icon files
4. **Create Shortcuts**: Optional - create desktop shortcuts with custom icons

### Browser Extensions: Managing Profiles

1. **Add Profile**: Click "+ Add Profile" and enter a name
2. **Switch Profile**: Click on any profile to switch
3. **Edit**: Click the edit button to rename
4. **Export**: Save profiles to JSON for backup
5. **Import**: Restore profiles from JSON file

### Using Icon Templates

```python
from icon_templates import get_template, get_templates_by_category

# Get a specific template
work_template = get_template("work")
print(f"{work_template['icon']} {work_template['name']} - {work_template['color']}")

# Get all professional templates
professional = get_templates_by_category("professional")

# Search for templates
dev_templates = search_templates("development")
```

## Project Structure

```
browser-profile-icons/
├── ProfilePop.py              # Original desktop app
├── ProfilePop_Modern.py       # Modern UI version
├── icon_templates.py          # Template library (NEW)
├── chrome-extension/          # Chrome extension (Simplified)
├── firefox-extension/         # Firefox extension (NEW)
├── edge-extension/            # Edge extension (NEW)
├── test_icon_templates.py     # Template tests (NEW)
├── test_profilepop_basic.py   # App tests (NEW)
├── pytest.ini                 # Test configuration (NEW)
├── requirements.txt           # Python dependencies
├── build_modern.py            # Build script
└── README.md                  # This file
```

## Requirements

### Desktop App
- Python 3.7+
- customtkinter
- Pillow (PIL)
- tkinter

### Browser Extensions
- Chrome 90+ / Edge 90+ (Chromium-based)
- Firefox 57+

### Development
- pytest (for running tests)

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest test_icon_templates.py

# Run with verbose output
pytest -v

# Run only unit tests
pytest -m unit
```

## Contributing

Contributions welcome! Priority areas:
1. Additional icon templates
2. UI/UX improvements
3. More tests
4. Documentation

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Extension not loading | Check manifest.json for errors, ensure Developer mode is enabled |
| Icons not generating | Ensure browser is closed during icon generation |
| Permission errors | Run as administrator on Windows |
| Import fails | Check JSON file format matches export format |

## Known Limitations

### What Works ✅
- Desktop icon generator with all features
- Chrome/Edge extensions with profile management
- Firefox extension with full functionality
- Icon template library with 26+ templates
- Export/Import in all extensions
- Keyboard shortcuts
- Cross-platform support (Windows/Mac/Linux)

### What Doesn't Work ❌
- Cloud synchronization (removed - was non-functional)
- Pro features/payment system (removed - was incomplete)
- Safari extension (Safari has restrictions)
- Automatic profile detection (browser APIs limited)

## Roadmap

### Completed ✅
- ✅ Firefox extension
- ✅ Icon template library
- ✅ Test suite
- ✅ Edge support
- ✅ Simplified extensions
- ✅ Better documentation

### Future Enhancements 🔮
- Search/filter in template gallery
- More icon templates (target: 50+)
- Template categories in UI
- Browser extension web store publishing
- Auto-update for templates
- Template creator tool

## License

MIT License - See [LICENSE](LICENSE) for details.

## Acknowledgments

- Python tkinter and customtkinter for GUI
- Pillow for image processing
- Mozilla/Chrome/Edge extension APIs

---

## Project Status

**Completion: ~90%** ✅ **v3.0 Release**

### What Works Now

**Desktop Application:**
- ✅ Full-featured Python GUI (ProfilePop_Modern.py)
- ✅ Icon generation with 5 shape options
- ✅ 20+ color palette with gradients
- ✅ Visual effects (shadow, glow, border, opacity)
- ✅ Multi-browser support (6+ browsers)
- ✅ Cross-platform (Windows/Mac/Linux)
- ✅ Settings persistence
- ✅ Export/Import profiles

**Browser Extensions:**
- ✅ Chrome extension (Manifest V3)
- ✅ Firefox extension (Manifest V2) - **NEW**
- ✅ Edge extension (Manifest V3) - **NEW**
- ✅ Profile management
- ✅ Quick switching (keyboard shortcuts)
- ✅ Export/Import functionality
- ✅ Settings page
- ✅ Context menu integration

**Development:**
- ✅ Icon template library (26+ templates) - **NEW**
- ✅ Test suite (pytest) - **NEW**
- ✅ Clean codebase (removed non-functional features)
- ✅ Comprehensive documentation

### Remaining 10%

**Polish & Enhancement:**
- ⚠️ Template gallery UI in desktop app
- ⚠️ More icon templates (target: 50+)
- ⚠️ Web store publishing
- ⚠️ Auto-update system for templates
- ⚠️ More comprehensive tests

**Nice-to-Have:**
- 🔮 Search/filter in extensions
- 🔮 Category-based browsing
- 🔮 Custom template creator
- 🔮 Browser extension sync (local, not cloud)

### What Changed in v3.0

**Removed (Non-Functional):**
- ❌ Cloud sync (fake API calls removed)
- ❌ Pro features/payment (incomplete licensing removed)
- ❌ Analytics tracking (unused code removed)

**Added (Fully Functional):**
- ✅ Firefox extension (complete implementation)
- ✅ Icon template library (26 templates)
- ✅ Test suite (comprehensive pytest tests)
- ✅ Edge extension (dedicated support)
- ✅ Simplified, focused feature set

### Current Status

**v3.0 is FEATURE COMPLETE** for core functionality:
- Desktop app works perfectly for icon generation
- All three browser extensions work reliably
- Template library provides quick-start options
- Tests verify functionality
- Documentation is comprehensive

The remaining 10% is polish, expansion, and nice-to-have features. The tool is fully usable and reliable in its current state.

---

**Author:** Wesley Ellis
**Website:** wesellis.com
**GitHub:** [wesellis/browser-profile-icons](https://github.com/wesellis/browser-profile-icons)

**Note:** This is a personal project for productivity. Core features are stable and tested. Use at your own discretion.
