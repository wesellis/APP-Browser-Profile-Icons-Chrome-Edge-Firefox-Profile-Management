# Browser Profile Icon Generator

A simple tool for creating custom icons for browser profiles in Chrome, Edge, and Firefox.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

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

**Author:** Wesley Ellis
**Note:** This is a utility tool for personal use. No guarantees or warranties provided.

