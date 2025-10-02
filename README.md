# Browser Profile Icon Generator

A tool for creating custom icons for browser profiles in Chrome, Edge, and Firefox.

[![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Stars](https://img.shields.io/github/stars/wesellis/APP-Browser-Profile-Icons-Chrome-Edge-Firefox-Profile-Management?style=flat-square)](https://github.com/wesellis/APP-Browser-Profile-Icons-Chrome-Edge-Firefox-Profile-Management/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/wesellis/APP-Browser-Profile-Icons-Chrome-Edge-Firefox-Profile-Management?style=flat-square)](https://github.com/wesellis/APP-Browser-Profile-Icons-Chrome-Edge-Firefox-Profile-Management/commits)

---

## Screenshot

![Browser Profile Icon Generator](docs/images/ProfilePop%20-%20Browser%20Profile%20Icon%20Generator%20-%20Main%20Window.png)

---

## What is This?

This is a personal project that helps you create custom icons for browser profiles. If you use multiple browser profiles (like separate profiles for work, personal, different clients, etc.), this tool makes it easier to visually identify them with custom icons.

## Features

- **Desktop App**: Python-based GUI for creating profile icons
- **Chrome Extension**: Browser extension for profile management
- **Icon Generation**: Create custom icons with text, colors, and shapes
- **Multiple Browsers**: Works with Chrome, Edge, and Firefox

## What's Included

### Desktop Application
- `ProfilePop.py` - Original icon generator
- `ProfilePop_Modern.py` - Updated version with modern UI
- Icon creation with custom text, colors, and shapes
- Various shape options (circle, rounded, square, etc.)

### Chrome Extension
Located in `chrome-extension/` directory:
- Profile switching functionality
- Custom icon management
- Browser integration

## Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)
- PIL/Pillow for image processing
- Chrome/Edge/Firefox browser

## Installation

```bash
# Clone the repository
git clone https://github.com/wesellis/browser-profile-icons.git
cd browser-profile-icons

# Install dependencies
pip install -r requirements.txt

# Run the application
python ProfilePop_Modern.py
```

### Installing the Chrome Extension

1. Open Chrome and go to `chrome://extensions`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `chrome-extension` folder from this project

## Usage

1. Run the desktop application
2. Enter text for your profile icon
3. Choose colors and shape style
4. Generate and save the icon
5. Set the icon for your browser profile

## Project Structure

```
.
├── ProfilePop.py           # Original application
├── ProfilePop_Modern.py    # Modern version
├── chrome-extension/       # Browser extension
├── logos/                  # Browser logos
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Building

```bash
# Build standalone executable
python build_modern.py
```

## Contributing

This is a personal project, but suggestions and improvements are welcome. Feel free to open an issue or pull request.

## License

MIT License - See [LICENSE](LICENSE) for details.

## Acknowledgments

- Python tkinter for the GUI framework
- Pillow for image processing

---

## Project Status & Roadmap

**Completion: ~75%**

### What Works
- ✅ Desktop icon generator (Python GUI)
- ✅ Chrome extension with basic profile switching
- ✅ Icon customization (shapes, colors, text, effects)
- ✅ Multiple shape options (circle, rounded, square, hexagon, badge)
- ✅ Visual effects (shadows, glow, borders, opacity)
- ✅ Cross-platform support (Windows, Mac, Linux paths)
- ✅ Settings persistence and profile management
- ✅ Build scripts for creating executables

### Known Limitations & Missing Features

**Browser Support:**
- ⚠️ **Firefox Extension**: Not yet implemented (claimed in project name but Chrome-only currently)
- ⚠️ **Edge Support**: Should work with Chrome extension but not explicitly tested
- ⚠️ **Profile automation**: Chrome extension manifest lists automation features that may not be fully implemented

**Advanced Features:**
- ⚠️ **Cloud Sync**: Listed in extension permissions but functionality not implemented
- ⚠️ **Profile Import/Export**: UI exists but may not be fully functional
- ⚠️ **Keyboard Shortcuts**: Defined in manifest but need testing
- ⚠️ **Icon Gallery/Templates**: Catalog exists but no built-in template library

**Code Quality:**
- ⚠️ **Testing**: No test suite despite pytest in requirements
- ⚠️ **Documentation**: Installation guide exists but could be more comprehensive
- ⚠️ **Error Handling**: Basic logging exists but needs more robust error recovery
- ⚠️ **Async Functions**: Uses async/await but may not be fully utilized

### What Needs Work

1. **Firefox Extension Development** - Create Firefox-compatible version
2. **Comprehensive Testing** - Add unit tests and integration tests
3. **Profile Synchronization** - Implement cloud sync functionality
4. **Better Documentation** - Step-by-step guides for all browsers
5. **Template Library** - Add pre-made icon templates/themes
6. **Edge-Specific Features** - Test and document Edge compatibility
7. **Error Recovery** - Better handling of browser path detection failures
8. **Performance Optimization** - Profile icon generation caching and optimization

### Contributing

If you'd like to help complete any of the missing features above, contributions are welcome. Priority areas:
1. Firefox extension development
2. Writing tests (pytest)
3. Improving documentation
4. Adding icon templates

---

**Author:** Wesley Ellis
**Note:** This is a utility tool for personal use. Core functionality works, but some advanced features are incomplete. No guarantees or warranties provided.

