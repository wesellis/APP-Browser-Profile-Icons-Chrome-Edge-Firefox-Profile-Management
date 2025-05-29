# ProfilePop - Browser Profile Icon Generator

<div align="center">

![ProfilePop](https://via.placeholder.com/100x100/5865f2/ffffff?text=PP)

**Generate custom icons for Edge, Firefox, and Chrome browser profiles**

[![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](#)
[![Portable](https://img.shields.io/badge/Portable-EXE-green?style=for-the-badge)](#)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

</div>

## ✨ Features

- 🎨 **Custom colored backgrounds** with 48-color palette
- 🌐 **Multi-browser support** - Edge, Firefox, and Chrome  
- 🖼️ **Browser logos** automatically embedded in icons
- 📝 **Profile names** with smart text contrast
- 🔧 **Desktop shortcuts** with custom icons
- 📌 **Taskbar-ready** icons with proper sizing
- 🚀 **Portable executable** - no installation required

## 🚀 Quick Start

### For End Users (Easiest)
1. **Download `ProfilePop.exe`** from [Releases](../../releases)
2. **Double-click to run** - no Python or installation needed!
3. **That's it!** The app is completely portable

### For Developers
1. **Clone this repository**
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run**: `python ProfilePop.py`

## 💻 System Requirements

**For the Portable EXE:**
- ✅ **Windows 10/11** (Windows 7/8 may work)
- ✅ **No Python installation needed**
- ✅ **No additional software required**
- ✅ **Works on any Windows PC**

**For Source Code:**
- Python 3.7+ with packages from `requirements.txt`

## 🎯 How to Use

1. **Launch ProfilePop** (double-click ProfilePop.exe)
2. **Select browser** (Edge, Firefox, or Chrome) from left panel
3. **Customize colors** - double-click profiles and choose colors
4. **Generate Icons** - creates .ico files with logos and names
5. **Create Shortcuts** - makes desktop shortcuts
6. **Pin to Taskbar** - right-click shortcuts → "Pin to taskbar"

## 🎨 Icon Preview

Your icons will look like:
- **Colored rounded backgrounds** in your chosen colors
- **Browser logos** (Edge/Firefox/Chrome) in the upper area
- **Profile names** below logos with smart contrast
- **Professional design** optimized for taskbar use

## 🛠️ Building from Source

To create your own executable:

```bash
# Method 1: Simple batch file
build.bat

# Method 2: Python script  
python build_exe.py
```

Both methods will:
- ✅ Convert your PNG icon to ICO format
- ✅ Bundle all dependencies into ProfilePop.exe
- ✅ Create a portable executable

## 📂 Project Structure

```
ProfilePop/
├── ProfilePop.py          # Main application
├── ProfilePop.vbs         # Silent launcher (for source)
├── ProfilePop_ICON.png    # App icon (PNG format)
├── logos/                 # Browser logo files
│   ├── microsoft-edge-browser-logo-blue-green-gradient-icon.png
│   ├── firefox-browser-logo-red-yellow-blue-circle-icon.png
│   └── google-chrome-logo-main-icon.png
├── build.bat             # Simple executable builder
├── build_exe.py          # Advanced build script
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## ❓ FAQ

**Q: Do I need Python installed to use ProfilePop.exe?**  
A: **No!** The .exe is completely portable and includes everything needed.

**Q: Will it work on computers without my software?**  
A: **Yes!** Just copy ProfilePop.exe to any Windows PC and run it.

**Q: What browsers are supported?**  
A: Microsoft Edge, Mozilla Firefox, and Google Chrome.

**Q: Can I customize the colors?**  
A: Yes! Choose from 48 colors, from dark themes to bright colors.

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Browser not found" | Install the browser or check if profiles exist |
| Icons look small in taskbar | Use latest version - we've fixed taskbar sizing |
| Permission errors | Close browser instances or run as administrator |
| Missing profiles | Create profiles in your browser first |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Browser logos are property of Microsoft, Mozilla, and Google respectively
- Built with Python, Tkinter, and Pillow
- Inspired by the Windows power user community

---

<div align="center">

**Made with ❤️ for organized browser profiles**

[⭐ Star this repo](../../stargazers) • [🐛 Report Bug](../../issues) • [💡 Request Feature](../../issues) • [📥 Download](../../releases)

</div>
