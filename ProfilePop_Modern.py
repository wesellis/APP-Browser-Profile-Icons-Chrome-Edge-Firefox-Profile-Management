"""
ProfilePop Modern - Browser Profile Icon Generator
Enhanced version with modern UI, advanced features, and cross-platform support
Author: Wesley Ellis
Version: 3.0.0
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import threading
import subprocess
import configparser
from functools import lru_cache
import io
import base64
from pathlib import Path
import hashlib
from datetime import datetime
import logging
from typing import Dict, List, Optional, Tuple
import asyncio
import aiofiles
import platform

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('profilepop.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Set modern theme
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Version info
__version__ = "3.0.0"
__app_name__ = "ProfilePop Modern"
__description__ = "Advanced Browser Profile Icon Generator"

class ModernProfilePop(ctk.CTk):
    """Modern ProfilePop application with enhanced UI and features"""
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title(f"{__app_name__} v{__version__}")
        self.geometry("1400x800")
        self.minsize(1200, 700)
        
        # Set window icon
        self.iconbitmap(default='ProfilePop_ICON.ico') if os.path.exists('ProfilePop_ICON.ico') else None
        
        # Initialize variables
        self.profiles: List[Dict] = []
        self.profile_colors: Dict = {}
        self.current_browser: Optional[str] = None
        self.selected_profile_index: Optional[int] = None
        self.theme_mode = "dark"
        
        # Browser paths
        self.browser_paths = self._detect_browser_paths()
        
        # Cache for images and performance
        self._image_cache: Dict = {}
        self._font_cache: Dict = {}
        self._icon_preview_cache: Dict = {}
        
        # Enhanced color palette with gradients
        self.color_palette = self._generate_enhanced_palette()
        
        # Icon shape options
        self.icon_shapes = ["rounded", "circle", "square", "hexagon", "badge"]
        self.current_shape = "rounded"
        
        # Font options
        self.font_options = ["Arial", "Segoe UI", "Helvetica", "Roboto", "Ubuntu"]
        self.current_font = "Segoe UI"
        
        # Initialize UI
        self._setup_ui()
        
        # Load saved settings
        self._load_settings()
        
        # Start background tasks
        self._start_background_tasks()
        
        logger.info(f"ProfilePop Modern v{__version__} initialized successfully")
    
    def _detect_browser_paths(self) -> Dict[str, str]:
        """Detect browser profile paths based on OS"""
        paths = {}
        
        if platform.system() == "Windows":
            paths = {
                "edge": os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data"),
                "firefox": os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox"),
                "chrome": os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data"),
                "brave": os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data"),
                "opera": os.path.expanduser("~\\AppData\\Roaming\\Opera Software\\Opera Stable"),
                "vivaldi": os.path.expanduser("~\\AppData\\Local\\Vivaldi\\User Data")
            }
        elif platform.system() == "Darwin":  # macOS
            paths = {
                "edge": os.path.expanduser("~/Library/Application Support/Microsoft Edge"),
                "firefox": os.path.expanduser("~/Library/Application Support/Firefox"),
                "chrome": os.path.expanduser("~/Library/Application Support/Google/Chrome"),
                "brave": os.path.expanduser("~/Library/Application Support/BraveSoftware/Brave-Browser"),
                "safari": os.path.expanduser("~/Library/Safari"),
                "opera": os.path.expanduser("~/Library/Application Support/com.operasoftware.Opera"),
                "vivaldi": os.path.expanduser("~/Library/Application Support/Vivaldi")
            }
        elif platform.system() == "Linux":
            paths = {
                "edge": os.path.expanduser("~/.config/microsoft-edge"),
                "firefox": os.path.expanduser("~/.mozilla/firefox"),
                "chrome": os.path.expanduser("~/.config/google-chrome"),
                "brave": os.path.expanduser("~/.config/BraveSoftware/Brave-Browser"),
                "opera": os.path.expanduser("~/.config/opera"),
                "vivaldi": os.path.expanduser("~/.config/vivaldi")
            }
        
        # Filter out non-existent paths
        return {k: v for k, v in paths.items() if os.path.exists(v)}
    
    def _generate_enhanced_palette(self) -> List[Dict]:
        """Generate enhanced color palette with gradients and themes"""
        base_colors = [
            # Dark theme colors
            {'name': 'Midnight', 'hex': '#10121c', 'gradient': ['#10121c', '#1e2139']},
            {'name': 'Purple Night', 'hex': '#2c1e31', 'gradient': ['#2c1e31', '#4a2c5e']},
            {'name': 'Wine', 'hex': '#6b2643', 'gradient': ['#6b2643', '#8e3556']},
            {'name': 'Ruby', 'hex': '#ac2847', 'gradient': ['#ac2847', '#d63760']},
            {'name': 'Crimson', 'hex': '#ec273f', 'gradient': ['#ec273f', '#ff4458']},
            
            # Earth tones
            {'name': 'Coffee', 'hex': '#4d3533', 'gradient': ['#4d3533', '#6b4c4a']},
            {'name': 'Caramel', 'hex': '#a26d3f', 'gradient': ['#a26d3f', '#c4854f']},
            {'name': 'Gold', 'hex': '#dab163', 'gradient': ['#dab163', '#f4d47c']},
            
            # Nature colors
            {'name': 'Forest', 'hex': '#1e4044', 'gradient': ['#1e4044', '#2e5a5f']},
            {'name': 'Emerald', 'hex': '#006554', 'gradient': ['#006554', '#008b6f']},
            {'name': 'Lime', 'hex': '#5ab552', 'gradient': ['#5ab552', '#7ed677']},
            
            # Ocean colors
            {'name': 'Deep Sea', 'hex': '#3e3b65', 'gradient': ['#3e3b65', '#514e88']},
            {'name': 'Ocean', 'hex': '#3859b3', 'gradient': ['#3859b3', '#4a6ed9']},
            {'name': 'Sky', 'hex': '#3388de', 'gradient': ['#3388de', '#5ca3f0']},
            {'name': 'Cyan', 'hex': '#36c5f4', 'gradient': ['#36c5f4', '#64d4f8']},
            
            # Pastel colors
            {'name': 'Lavender', 'hex': '#b0a7b8', 'gradient': ['#b0a7b8', '#d0c7d8']},
            {'name': 'Rose', 'hex': '#ffa2ac', 'gradient': ['#ffa2ac', '#ffbec6']},
            {'name': 'Peach', 'hex': '#ffd1d5', 'gradient': ['#ffd1d5', '#ffe5e8']},
            
            # Monochrome
            {'name': 'Pure White', 'hex': '#ffffff', 'gradient': ['#ffffff', '#f5f5f5']},
            {'name': 'Light Gray', 'hex': '#e0e0e0', 'gradient': ['#e0e0e0', '#c0c0c0']},
            {'name': 'Dark Gray', 'hex': '#404040', 'gradient': ['#404040', '#606060']},
            {'name': 'Black', 'hex': '#000000', 'gradient': ['#000000', '#1a1a1a']}
        ]
        
        return base_colors
    
    def _setup_ui(self):
        """Setup the modern UI with CustomTkinter"""
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Main container
        self.main_container = ctk.CTkFrame(self)
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        # Left sidebar
        self._create_sidebar()
        
        # Center content area
        self._create_content_area()
        
        # Right panel
        self._create_right_panel()
        
        # Bottom status bar
        self._create_status_bar()
        
        # Floating action buttons
        self._create_floating_buttons()
    
    def _create_sidebar(self):
        """Create modern sidebar with browser selection"""
        self.sidebar = ctk.CTkFrame(self.main_container, width=250)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.sidebar.grid_propagate(False)
        
        # App logo and title
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=20)
        
        title_label = ctk.CTkLabel(
            logo_frame,
            text=__app_name__,
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack()
        
        version_label = ctk.CTkLabel(
            logo_frame,
            text=f"v{__version__}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        version_label.pack()
        
        # Theme toggle
        self.theme_switch = ctk.CTkSwitch(
            self.sidebar,
            text="Dark Mode",
            command=self._toggle_theme,
            onvalue="dark",
            offvalue="light"
        )
        self.theme_switch.pack(pady=10)
        self.theme_switch.select()
        
        # Browser selection
        browser_label = ctk.CTkLabel(
            self.sidebar,
            text="Select Browser",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        browser_label.pack(pady=(20, 10))
        
        # Browser buttons with icons
        self.browser_frame = ctk.CTkScrollableFrame(self.sidebar, height=400)
        self.browser_frame.pack(fill="both", expand=True, padx=10)
        
        browser_info = {
            "chrome": {"name": "Google Chrome", "icon": "🌐", "color": "#4285F4"},
            "edge": {"name": "Microsoft Edge", "icon": "🌊", "color": "#0078D4"},
            "firefox": {"name": "Mozilla Firefox", "icon": "🦊", "color": "#FF7139"},
            "brave": {"name": "Brave Browser", "icon": "🦁", "color": "#FB542B"},
            "opera": {"name": "Opera", "icon": "🎭", "color": "#FF1B2D"},
            "vivaldi": {"name": "Vivaldi", "icon": "🎨", "color": "#EF3939"},
            "safari": {"name": "Safari", "icon": "🧭", "color": "#006CFF"}
        }
        
        for browser_key, browser_path in self.browser_paths.items():
            if browser_key in browser_info:
                info = browser_info[browser_key]
                btn = ctk.CTkButton(
                    self.browser_frame,
                    text=f"{info['icon']} {info['name']}",
                    command=lambda b=browser_key: self._load_browser_profiles(b),
                    height=50,
                    font=ctk.CTkFont(size=14),
                    fg_color=info['color'],
                    hover_color=self._adjust_color_brightness(info['color'], 0.8)
                )
                btn.pack(pady=5, fill="x")
        
        # Settings button
        self.settings_btn = ctk.CTkButton(
            self.sidebar,
            text="⚙️ Settings",
            command=self._open_settings,
            height=40
        )
        self.settings_btn.pack(side="bottom", pady=10, fill="x", padx=10)
    
    def _create_content_area(self):
        """Create main content area with profile management"""
        self.content_area = ctk.CTkFrame(self.main_container)
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=(0, 10))
        self.content_area.grid_columnconfigure(0, weight=1)
        self.content_area.grid_rowconfigure(1, weight=1)
        
        # Header
        header_frame = ctk.CTkFrame(self.content_area, height=60)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header_frame.grid_columnconfigure(1, weight=1)
        
        self.header_label = ctk.CTkLabel(
            header_frame,
            text="Select a browser to manage profiles",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.header_label.grid(row=0, column=0, padx=20, pady=15)
        
        # Search bar
        self.search_var = tk.StringVar()
        self.search_entry = ctk.CTkEntry(
            header_frame,
            placeholder_text="🔍 Search profiles...",
            textvariable=self.search_var,
            width=300
        )
        self.search_entry.grid(row=0, column=1, padx=20, pady=15, sticky="e")
        self.search_var.trace("w", self._filter_profiles)
        
        # Profile grid
        self.profile_container = ctk.CTkScrollableFrame(self.content_area)
        self.profile_container.grid(row=1, column=0, sticky="nsew", padx=10)
        self.profile_container.grid_columnconfigure(0, weight=1)
        
        # Action buttons
        action_frame = ctk.CTkFrame(self.content_area, height=80)
        action_frame.grid(row=2, column=0, sticky="ew", pady=10)
        
        self.generate_btn = ctk.CTkButton(
            action_frame,
            text="🎨 Generate All Icons",
            command=self._generate_all_icons,
            height=50,
            width=200,
            font=ctk.CTkFont(size=16, weight="bold"),
            state="disabled"
        )
        self.generate_btn.pack(side="left", padx=10)
        
        self.create_shortcuts_btn = ctk.CTkButton(
            action_frame,
            text="🔗 Create Shortcuts",
            command=self._create_shortcuts,
            height=50,
            width=200,
            font=ctk.CTkFont(size=16, weight="bold"),
            state="disabled"
        )
        self.create_shortcuts_btn.pack(side="left", padx=10)
        
        self.export_btn = ctk.CTkButton(
            action_frame,
            text="📦 Export Profile Pack",
            command=self._export_profiles,
            height=50,
            width=200,
            font=ctk.CTkFont(size=16, weight="bold"),
            state="disabled"
        )
        self.export_btn.pack(side="left", padx=10)
    
    def _create_right_panel(self):
        """Create right panel with customization options"""
        self.right_panel = ctk.CTkFrame(self.main_container, width=350)
        self.right_panel.grid(row=0, column=2, sticky="nsew")
        self.right_panel.grid_propagate(False)
        
        # Preview section
        preview_label = ctk.CTkLabel(
            self.right_panel,
            text="Icon Preview",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        preview_label.pack(pady=10)
        
        self.preview_frame = ctk.CTkFrame(self.right_panel, height=200)
        self.preview_frame.pack(padx=20, pady=10, fill="x")
        
        self.preview_canvas = ctk.CTkCanvas(
            self.preview_frame,
            width=180,
            height=180,
            bg="gray20",
            highlightthickness=0
        )
        self.preview_canvas.pack(pady=10)
        
        # Customization tabs
        self.custom_tabview = ctk.CTkTabview(self.right_panel)
        self.custom_tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Color tab
        self.custom_tabview.add("Colors")
        self._create_color_tab()
        
        # Shape tab
        self.custom_tabview.add("Shape")
        self._create_shape_tab()
        
        # Text tab
        self.custom_tabview.add("Text")
        self._create_text_tab()
        
        # Effects tab
        self.custom_tabview.add("Effects")
        self._create_effects_tab()
    
    def _create_color_tab(self):
        """Create color customization tab"""
        color_tab = self.custom_tabview.tab("Colors")
        
        # Color mode selection
        mode_label = ctk.CTkLabel(color_tab, text="Color Mode:")
        mode_label.pack(pady=5)
        
        self.color_mode = ctk.CTkSegmentedButton(
            color_tab,
            values=["Solid", "Gradient", "Pattern"],
            command=self._update_color_mode
        )
        self.color_mode.pack(pady=10)
        self.color_mode.set("Gradient")
        
        # Color palette
        palette_frame = ctk.CTkScrollableFrame(color_tab, height=300)
        palette_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        colors_per_row = 6
        for i, color_info in enumerate(self.color_palette):
            row = i // colors_per_row
            col = i % colors_per_row
            
            color_btn = tk.Button(
                palette_frame,
                bg=color_info['hex'],
                width=4,
                height=2,
                relief="flat",
                command=lambda c=color_info: self._select_color(c)
            )
            color_btn.grid(row=row, column=col, padx=2, pady=2)
        
        # Custom color picker
        self.custom_color_btn = ctk.CTkButton(
            color_tab,
            text="🎨 Custom Color",
            command=self._pick_custom_color,
            height=40
        )
        self.custom_color_btn.pack(pady=10, fill="x", padx=10)
    
    def _create_shape_tab(self):
        """Create shape customization tab"""
        shape_tab = self.custom_tabview.tab("Shape")
        
        shape_label = ctk.CTkLabel(shape_tab, text="Icon Shape:")
        shape_label.pack(pady=10)
        
        for shape in self.icon_shapes:
            shape_btn = ctk.CTkRadioButton(
                shape_tab,
                text=shape.capitalize(),
                variable=tk.StringVar(value=self.current_shape),
                value=shape,
                command=lambda s=shape: self._set_shape(s)
            )
            shape_btn.pack(pady=5)
        
        # Corner radius slider for rounded shape
        self.radius_label = ctk.CTkLabel(shape_tab, text="Corner Radius:")
        self.radius_label.pack(pady=(20, 5))
        
        self.radius_slider = ctk.CTkSlider(
            shape_tab,
            from_=0,
            to=50,
            command=self._update_radius
        )
        self.radius_slider.pack(pady=5, fill="x", padx=20)
        self.radius_slider.set(25)
    
    def _create_text_tab(self):
        """Create text customization tab"""
        text_tab = self.custom_tabview.tab("Text")
        
        # Font selection
        font_label = ctk.CTkLabel(text_tab, text="Font Family:")
        font_label.pack(pady=10)
        
        self.font_menu = ctk.CTkOptionMenu(
            text_tab,
            values=self.font_options,
            command=self._update_font
        )
        self.font_menu.pack(pady=5, fill="x", padx=20)
        
        # Font size
        size_label = ctk.CTkLabel(text_tab, text="Font Size:")
        size_label.pack(pady=10)
        
        self.font_size_slider = ctk.CTkSlider(
            text_tab,
            from_=8,
            to=24,
            command=self._update_font_size
        )
        self.font_size_slider.pack(pady=5, fill="x", padx=20)
        self.font_size_slider.set(14)
        
        # Text position
        pos_label = ctk.CTkLabel(text_tab, text="Text Position:")
        pos_label.pack(pady=10)
        
        self.text_position = ctk.CTkSegmentedButton(
            text_tab,
            values=["Bottom", "Center", "Top"],
            command=self._update_text_position
        )
        self.text_position.pack(pady=10)
        self.text_position.set("Bottom")
        
        # Show/hide text
        self.show_text_var = tk.BooleanVar(value=True)
        self.show_text_check = ctk.CTkCheckBox(
            text_tab,
            text="Show Profile Name",
            variable=self.show_text_var,
            command=self._update_preview
        )
        self.show_text_check.pack(pady=10)
    
    def _create_effects_tab(self):
        """Create effects customization tab"""
        effects_tab = self.custom_tabview.tab("Effects")
        
        # Shadow effect
        self.shadow_var = tk.BooleanVar(value=True)
        self.shadow_check = ctk.CTkCheckBox(
            effects_tab,
            text="Drop Shadow",
            variable=self.shadow_var,
            command=self._update_preview
        )
        self.shadow_check.pack(pady=10)
        
        # Glow effect
        self.glow_var = tk.BooleanVar(value=False)
        self.glow_check = ctk.CTkCheckBox(
            effects_tab,
            text="Glow Effect",
            variable=self.glow_var,
            command=self._update_preview
        )
        self.glow_check.pack(pady=10)
        
        # Border
        self.border_var = tk.BooleanVar(value=False)
        self.border_check = ctk.CTkCheckBox(
            effects_tab,
            text="Border",
            variable=self.border_var,
            command=self._update_preview
        )
        self.border_check.pack(pady=10)
        
        # Opacity
        opacity_label = ctk.CTkLabel(effects_tab, text="Icon Opacity:")
        opacity_label.pack(pady=10)
        
        self.opacity_slider = ctk.CTkSlider(
            effects_tab,
            from_=50,
            to=100,
            command=self._update_opacity
        )
        self.opacity_slider.pack(pady=5, fill="x", padx=20)
        self.opacity_slider.set(100)
    
    def _create_status_bar(self):
        """Create status bar at bottom"""
        self.status_bar = ctk.CTkFrame(self, height=30)
        self.status_bar.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="Ready",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="left", padx=10)
        
        self.progress_bar = ctk.CTkProgressBar(self.status_bar)
        self.progress_bar.pack(side="right", padx=10)
        self.progress_bar.set(0)
    
    def _create_floating_buttons(self):
        """Create floating action buttons"""
        # Import profiles button
        self.import_btn = ctk.CTkButton(
            self,
            text="📥",
            command=self._import_profiles,
            width=50,
            height=50,
            corner_radius=25,
            font=ctk.CTkFont(size=20)
        )
        self.import_btn.place(relx=0.95, rely=0.85, anchor="center")
        
        # Help button
        self.help_btn = ctk.CTkButton(
            self,
            text="❓",
            command=self._show_help,
            width=50,
            height=50,
            corner_radius=25,
            font=ctk.CTkFont(size=20)
        )
        self.help_btn.place(relx=0.95, rely=0.93, anchor="center")
    
    def _toggle_theme(self):
        """Toggle between dark and light theme"""
        if self.theme_switch.get() == "dark":
            ctk.set_appearance_mode("dark")
            self.theme_mode = "dark"
        else:
            ctk.set_appearance_mode("light")
            self.theme_mode = "light"
        
        self._update_preview()
        logger.info(f"Theme switched to {self.theme_mode}")
    
    def _load_browser_profiles(self, browser: str):
        """Load profiles for selected browser"""
        self.current_browser = browser
        self.profiles = []
        
        # Update header
        browser_names = {
            "chrome": "Google Chrome",
            "edge": "Microsoft Edge",
            "firefox": "Mozilla Firefox",
            "brave": "Brave Browser",
            "opera": "Opera",
            "vivaldi": "Vivaldi",
            "safari": "Safari"
        }
        
        self.header_label.configure(text=f"{browser_names.get(browser, browser)} Profiles")
        self._update_status(f"Loading {browser_names.get(browser)} profiles...")
        
        # Load profiles in background thread
        threading.Thread(target=self._load_profiles_async, args=(browser,), daemon=True).start()
    
    def _load_profiles_async(self, browser: str):
        """Load browser profiles asynchronously"""
        try:
            if browser == "firefox":
                self._load_firefox_profiles()
            else:
                self._load_chromium_profiles(browser)
            
            # Update UI in main thread
            self.after(0, self._display_profiles)
            self.after(0, lambda: self._update_status(f"Loaded {len(self.profiles)} profiles"))
            
        except Exception as e:
            logger.error(f"Error loading profiles: {e}")
            self.after(0, lambda: messagebox.showerror("Error", f"Failed to load profiles: {str(e)}"))
    
    def _load_chromium_profiles(self, browser: str):
        """Load Chromium-based browser profiles"""
        browser_path = self.browser_paths.get(browser)
        if not browser_path:
            return
        
        # Load Local State file
        local_state_path = os.path.join(browser_path, "Local State")
        if not os.path.exists(local_state_path):
            return
        
        with open(local_state_path, 'r', encoding='utf-8') as f:
            local_state = json.load(f)
        
        # Get profile info
        profile_info = local_state.get('profile', {}).get('info_cache', {})
        
        for profile_id, profile_data in profile_info.items():
            self.profiles.append({
                'id': profile_id,
                'name': profile_data.get('name', profile_id),
                'path': os.path.join(browser_path, profile_id),
                'color': self._get_random_color(),
                'browser': browser
            })
    
    def _load_firefox_profiles(self):
        """Load Firefox profiles"""
        firefox_path = self.browser_paths.get("firefox")
        if not firefox_path:
            return
        
        profiles_ini = os.path.join(firefox_path, "profiles.ini")
        if not os.path.exists(profiles_ini):
            return
        
        config = configparser.ConfigParser()
        config.read(profiles_ini)
        
        for section in config.sections():
            if section.startswith("Profile"):
                profile_name = config.get(section, "Name", fallback="Unknown")
                profile_path = config.get(section, "Path", fallback="")
                
                if profile_path:
                    self.profiles.append({
                        'id': section,
                        'name': profile_name,
                        'path': os.path.join(firefox_path, profile_path),
                        'color': self._get_random_color(),
                        'browser': 'firefox'
                    })
    
    def _display_profiles(self):
        """Display loaded profiles in grid"""
        # Clear existing profile widgets
        for widget in self.profile_container.winfo_children():
            widget.destroy()
        
        if not self.profiles:
            no_profiles_label = ctk.CTkLabel(
                self.profile_container,
                text="No profiles found for this browser",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            no_profiles_label.pack(pady=50)
            return
        
        # Enable action buttons
        self.generate_btn.configure(state="normal")
        self.create_shortcuts_btn.configure(state="normal")
        self.export_btn.configure(state="normal")
        
        # Create profile cards
        columns = 3
        for i, profile in enumerate(self.profiles):
            row = i // columns
            col = i % columns
            
            # Profile card
            card = ctk.CTkFrame(self.profile_container, corner_radius=10)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Profile icon preview
            icon_frame = ctk.CTkFrame(card, width=100, height=100)
            icon_frame.pack(pady=10)
            
            # Generate mini preview
            self._generate_mini_preview(icon_frame, profile)
            
            # Profile name
            name_label = ctk.CTkLabel(
                card,
                text=profile['name'],
                font=ctk.CTkFont(size=14, weight="bold")
            )
            name_label.pack(pady=5)
            
            # Color selector
            color_btn = ctk.CTkButton(
                card,
                text="Change Color",
                command=lambda p=profile: self._change_profile_color(p),
                height=30
            )
            color_btn.pack(pady=5, padx=10, fill="x")
            
            # Edit button
            edit_btn = ctk.CTkButton(
                card,
                text="✏️ Edit",
                command=lambda p=profile, idx=i: self._edit_profile(p, idx),
                height=30
            )
            edit_btn.pack(pady=5, padx=10, fill="x")
    
    def _generate_mini_preview(self, parent, profile):
        """Generate mini icon preview for profile card"""
        # Create small icon
        size = 80
        icon = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(icon)
        
        # Get color
        color = profile.get('color', '#3388de')
        if isinstance(color, dict):
            # Gradient support
            color = color.get('hex', '#3388de')
        
        # Draw shape
        if self.current_shape == "circle":
            draw.ellipse([0, 0, size-1, size-1], fill=color)
        elif self.current_shape == "rounded":
            self._draw_rounded_rectangle(draw, [0, 0, size-1, size-1], 15, color)
        else:
            draw.rectangle([0, 0, size-1, size-1], fill=color)
        
        # Add browser logo (simplified)
        browser_icons = {
            'chrome': '🌐',
            'edge': '🌊',
            'firefox': '🦊',
            'brave': '🦁',
            'opera': '🎭',
            'vivaldi': '🎨',
            'safari': '🧭'
        }
        
        # Convert to PhotoImage and display
        # Note: This is simplified - in production you'd properly convert and display
        canvas = tk.Canvas(parent, width=size, height=size, highlightthickness=0)
        canvas.pack()
        
        # Draw colored background
        if self.current_shape == "circle":
            canvas.create_oval(0, 0, size, size, fill=color, outline="")
        else:
            canvas.create_rectangle(0, 0, size, size, fill=color, outline="")
        
        # Add browser emoji
        browser = profile.get('browser', 'chrome')
        emoji = browser_icons.get(browser, '🌐')
        canvas.create_text(size//2, size//2 - 10, text=emoji, font=("Arial", 24))
        
        # Add profile name
        if self.show_text_var.get():
            name = profile['name'][:8] + "..." if len(profile['name']) > 8 else profile['name']
            canvas.create_text(size//2, size - 10, text=name, font=("Arial", 8), fill="white")
    
    def _change_profile_color(self, profile):
        """Change color for specific profile"""
        color = colorchooser.askcolor(initialcolor=profile.get('color', '#3388de'))
        if color[1]:
            profile['color'] = color[1]
            self._display_profiles()
            self._update_preview()
    
    def _edit_profile(self, profile, index):
        """Edit profile details"""
        self.selected_profile_index = index
        self._update_preview()
        
        # Show edit dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Edit Profile: {profile['name']}")
        dialog.geometry("400x300")
        
        # Name field
        name_label = ctk.CTkLabel(dialog, text="Profile Name:")
        name_label.pack(pady=10)
        
        name_var = tk.StringVar(value=profile['name'])
        name_entry = ctk.CTkEntry(dialog, textvariable=name_var)
        name_entry.pack(pady=5, padx=20, fill="x")
        
        # Save button
        def save_changes():
            profile['name'] = name_var.get()
            self._display_profiles()
            dialog.destroy()
        
        save_btn = ctk.CTkButton(dialog, text="Save", command=save_changes)
        save_btn.pack(pady=20)
    
    def _generate_all_icons(self):
        """Generate icons for all profiles"""
        if not self.profiles:
            return
        
        # Create output directory
        output_dir = f"ProfileIcons_{self.current_browser}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(output_dir, exist_ok=True)
        
        self._update_status(f"Generating {len(self.profiles)} icons...")
        self.progress_bar.set(0)
        
        # Generate icons in background
        threading.Thread(
            target=self._generate_icons_async,
            args=(output_dir,),
            daemon=True
        ).start()
    
    def _generate_icons_async(self, output_dir):
        """Generate icons asynchronously"""
        try:
            total = len(self.profiles)
            for i, profile in enumerate(self.profiles):
                # Generate icon
                icon_path = self._generate_single_icon(profile, output_dir)
                
                # Update progress
                progress = (i + 1) / total
                self.after(0, lambda p=progress: self.progress_bar.set(p))
                self.after(0, lambda: self._update_status(f"Generated {i+1}/{total} icons"))
            
            # Complete
            self.after(0, lambda: self._update_status(f"✅ Generated {total} icons in {output_dir}"))
            self.after(0, lambda: messagebox.showinfo("Success", f"Icons generated successfully!\nLocation: {output_dir}"))
            
        except Exception as e:
            logger.error(f"Error generating icons: {e}")
            self.after(0, lambda: messagebox.showerror("Error", f"Failed to generate icons: {str(e)}"))
    
    def _generate_single_icon(self, profile, output_dir):
        """Generate a single icon file"""
        sizes = [16, 32, 48, 128, 256]
        icon_images = []
        
        for size in sizes:
            # Create icon image
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Get color
            color = profile.get('color', '#3388de')
            if isinstance(color, dict):
                color = color.get('hex', '#3388de')
            
            # Draw background shape
            if self.current_shape == "circle":
                draw.ellipse([0, 0, size-1, size-1], fill=color)
            elif self.current_shape == "rounded":
                radius = int(size * 0.2)
                self._draw_rounded_rectangle(draw, [0, 0, size-1, size-1], radius, color)
            elif self.current_shape == "hexagon":
                self._draw_hexagon(draw, size, color)
            else:
                draw.rectangle([0, 0, size-1, size-1], fill=color)
            
            # Add effects
            if self.shadow_var.get():
                img = self._add_shadow(img)
            
            if self.glow_var.get():
                img = self._add_glow(img, color)
            
            # Add browser logo
            logo_path = f"logos/{profile['browser']}-logo.png"
            if os.path.exists(logo_path):
                logo = Image.open(logo_path)
                logo_size = int(size * 0.5)
                logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                
                # Paste logo
                logo_pos = ((size - logo_size) // 2, (size - logo_size) // 2 - int(size * 0.1))
                img.paste(logo, logo_pos, logo)
            
            # Add text
            if self.show_text_var.get() and size >= 48:
                self._add_text_to_icon(draw, profile['name'], size)
            
            icon_images.append(img)
        
        # Save as ICO
        output_path = os.path.join(output_dir, f"{profile['name'].replace(' ', '_')}.ico")
        icon_images[0].save(output_path, format='ICO', sizes=[(s, s) for s in sizes])
        
        return output_path
    
    def _draw_rounded_rectangle(self, draw, coords, radius, fill):
        """Draw a rounded rectangle"""
        x1, y1, x2, y2 = coords
        
        # Draw rectangles and circles for rounded corners
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
        
        draw.ellipse([x1, y1, x1 + radius * 2, y1 + radius * 2], fill=fill)
        draw.ellipse([x2 - radius * 2, y1, x2, y1 + radius * 2], fill=fill)
        draw.ellipse([x1, y2 - radius * 2, x1 + radius * 2, y2], fill=fill)
        draw.ellipse([x2 - radius * 2, y2 - radius * 2, x2, y2], fill=fill)
    
    def _draw_hexagon(self, draw, size, fill):
        """Draw a hexagon shape"""
        center = size // 2
        radius = size // 2 - 2
        
        points = []
        for i in range(6):
            angle = i * 60 * 3.14159 / 180
            x = center + radius * cos(angle)
            y = center + radius * sin(angle)
            points.append((x, y))
        
        draw.polygon(points, fill=fill)
    
    def _add_shadow(self, img):
        """Add drop shadow effect"""
        # Create shadow
        shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        
        # Draw shadow shape (simplified)
        size = img.size[0]
        offset = 2
        shadow_draw.ellipse([offset, offset, size-1, size-1], fill=(0, 0, 0, 100))
        
        # Blur shadow
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=3))
        
        # Composite
        result = Image.new('RGBA', img.size, (0, 0, 0, 0))
        result.paste(shadow, (0, 0))
        result.paste(img, (0, 0), img)
        
        return result
    
    def _add_glow(self, img, color):
        """Add glow effect"""
        # Create glow
        glow = img.copy()
        glow = glow.filter(ImageFilter.GaussianBlur(radius=5))
        
        # Enhance glow color
        enhancer = ImageEnhance.Brightness(glow)
        glow = enhancer.enhance(1.5)
        
        # Composite
        result = Image.new('RGBA', img.size, (0, 0, 0, 0))
        result.paste(glow, (0, 0))
        result.paste(img, (0, 0), img)
        
        return result
    
    def _add_text_to_icon(self, draw, text, size):
        """Add text to icon"""
        try:
            # Load font
            font_size = int(size * 0.15)
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Calculate text position
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (size - text_width) // 2
        y = size - text_height - int(size * 0.1)
        
        # Draw text with outline for visibility
        outline_color = "black" if self._is_light_color(self.profiles[0].get('color', '#ffffff')) else "white"
        
        # Draw outline
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
        
        # Draw text
        text_color = "white" if not self._is_light_color(self.profiles[0].get('color', '#ffffff')) else "black"
        draw.text((x, y), text, font=font, fill=text_color)
    
    def _is_light_color(self, hex_color):
        """Check if color is light or dark"""
        if isinstance(hex_color, dict):
            hex_color = hex_color.get('hex', '#ffffff')
        
        # Convert hex to RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Calculate luminance
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        
        return luminance > 0.5
    
    def _create_shortcuts(self):
        """Create desktop shortcuts for profiles"""
        if not self.profiles or not self.current_browser:
            return
        
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        browser_exe = self._get_browser_executable(self.current_browser)
        
        if not browser_exe:
            messagebox.showerror("Error", "Browser executable not found")
            return
        
        created = 0
        for profile in self.profiles:
            try:
                # Create shortcut (Windows specific - needs pywin32)
                import win32com.client
                
                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut_path = os.path.join(desktop, f"{profile['name']} - {self.current_browser.title()}.lnk")
                shortcut = shell.CreateShortCut(shortcut_path)
                
                # Set shortcut properties
                shortcut.Targetpath = browser_exe
                
                if self.current_browser == "firefox":
                    shortcut.Arguments = f'-P "{profile["name"]}"'
                else:
                    shortcut.Arguments = f'--profile-directory="{profile["id"]}"'
                
                # Set icon if generated
                icon_path = f"ProfileIcons_{self.current_browser}*/{profile['name'].replace(' ', '_')}.ico"
                import glob
                icon_files = glob.glob(icon_path)
                if icon_files:
                    shortcut.IconLocation = os.path.abspath(icon_files[0])
                
                shortcut.save()
                created += 1
                
            except Exception as e:
                logger.error(f"Error creating shortcut for {profile['name']}: {e}")
        
        if created > 0:
            messagebox.showinfo("Success", f"Created {created} desktop shortcuts")
    
    def _get_browser_executable(self, browser):
        """Get browser executable path"""
        if platform.system() == "Windows":
            paths = {
                "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
                "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
                "opera": r"C:\Program Files\Opera\opera.exe",
                "vivaldi": r"C:\Program Files\Vivaldi\Application\vivaldi.exe"
            }
        elif platform.system() == "Darwin":
            paths = {
                "chrome": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "edge": "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
                "firefox": "/Applications/Firefox.app/Contents/MacOS/firefox",
                "brave": "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
                "safari": "/Applications/Safari.app/Contents/MacOS/Safari",
                "opera": "/Applications/Opera.app/Contents/MacOS/Opera",
                "vivaldi": "/Applications/Vivaldi.app/Contents/MacOS/Vivaldi"
            }
        else:  # Linux
            paths = {
                "chrome": "/usr/bin/google-chrome-stable",
                "edge": "/usr/bin/microsoft-edge",
                "firefox": "/usr/bin/firefox",
                "brave": "/usr/bin/brave-browser",
                "opera": "/usr/bin/opera",
                "vivaldi": "/usr/bin/vivaldi"
            }
        
        exe_path = paths.get(browser)
        if exe_path and os.path.exists(exe_path):
            return exe_path
        
        # Try to find in PATH
        import shutil
        return shutil.which(browser)
    
    def _export_profiles(self):
        """Export profile configuration"""
        if not self.profiles:
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            export_data = {
                "version": __version__,
                "browser": self.current_browser,
                "profiles": self.profiles,
                "settings": {
                    "shape": self.current_shape,
                    "font": self.current_font,
                    "show_text": self.show_text_var.get(),
                    "effects": {
                        "shadow": self.shadow_var.get(),
                        "glow": self.glow_var.get(),
                        "border": self.border_var.get()
                    }
                }
            }
            
            with open(file_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            messagebox.showinfo("Success", f"Profiles exported to {file_path}")
    
    def _import_profiles(self):
        """Import profile configuration"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    import_data = json.load(f)
                
                # Load profiles
                self.profiles = import_data.get("profiles", [])
                self.current_browser = import_data.get("browser", "chrome")
                
                # Load settings
                settings = import_data.get("settings", {})
                self.current_shape = settings.get("shape", "rounded")
                self.current_font = settings.get("font", "Segoe UI")
                self.show_text_var.set(settings.get("show_text", True))
                
                effects = settings.get("effects", {})
                self.shadow_var.set(effects.get("shadow", True))
                self.glow_var.set(effects.get("glow", False))
                self.border_var.set(effects.get("border", False))
                
                # Update UI
                self._display_profiles()
                messagebox.showinfo("Success", f"Imported {len(self.profiles)} profiles")
                
            except Exception as e:
                logger.error(f"Error importing profiles: {e}")
                messagebox.showerror("Error", f"Failed to import profiles: {str(e)}")
    
    def _open_settings(self):
        """Open settings dialog"""
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Settings")
        settings_window.geometry("600x500")
        
        # Settings tabs
        tabview = ctk.CTkTabview(settings_window)
        tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # General tab
        tabview.add("General")
        general_tab = tabview.tab("General")
        
        # Auto-save setting
        auto_save_var = tk.BooleanVar(value=True)
        auto_save_check = ctk.CTkCheckBox(
            general_tab,
            text="Auto-save settings",
            variable=auto_save_var
        )
        auto_save_check.pack(pady=10)
        
        # Default browser
        default_browser_label = ctk.CTkLabel(general_tab, text="Default Browser:")
        default_browser_label.pack(pady=5)
        
        default_browser_menu = ctk.CTkOptionMenu(
            general_tab,
            values=list(self.browser_paths.keys())
        )
        default_browser_menu.pack(pady=5)
        
        # Advanced tab
        tabview.add("Advanced")
        advanced_tab = tabview.tab("Advanced")
        
        # Cache settings
        clear_cache_btn = ctk.CTkButton(
            advanced_tab,
            text="Clear Icon Cache",
            command=self._clear_cache
        )
        clear_cache_btn.pack(pady=10)
        
        # Export/Import settings
        export_settings_btn = ctk.CTkButton(
            advanced_tab,
            text="Export Settings",
            command=self._export_settings
        )
        export_settings_btn.pack(pady=10)
        
        import_settings_btn = ctk.CTkButton(
            advanced_tab,
            text="Import Settings",
            command=self._import_settings
        )
        import_settings_btn.pack(pady=10)
        
        # About tab
        tabview.add("About")
        about_tab = tabview.tab("About")
        
        about_text = f"""
{__app_name__}
Version: {__version__}

{__description__}

Author: Wesley Ellis
Website: wesellis.com

© 2025 Wesley Ellis
Licensed under MIT License
        """
        
        about_label = ctk.CTkLabel(
            about_tab,
            text=about_text,
            justify="center"
        )
        about_label.pack(pady=20)
    
    def _show_help(self):
        """Show help dialog"""
        help_window = ctk.CTkToplevel(self)
        help_window.title("Help")
        help_window.geometry("700x600")
        
        # Help content
        help_text = """
ProfilePop Modern - Help Guide

🚀 QUICK START:
1. Select your browser from the left sidebar
2. Customize colors and appearance for each profile
3. Click "Generate All Icons" to create icon files
4. Click "Create Shortcuts" to add desktop shortcuts

🎨 CUSTOMIZATION:
• Colors: Choose from palette or use custom colors
• Shapes: Circle, rounded, square, hexagon, badge
• Text: Customize font, size, and position
• Effects: Add shadows, glow, borders

⌨️ KEYBOARD SHORTCUTS:
• Ctrl+G: Generate icons
• Ctrl+S: Save settings
• Ctrl+E: Export profiles
• Ctrl+I: Import profiles
• F1: Show this help

💡 TIPS:
• Double-click profiles to edit names
• Drag to reorder profiles
• Right-click for context menu options
• Use gradients for modern look

🔧 TROUBLESHOOTING:
• Ensure browser is closed when generating icons
• Run as administrator if permission errors occur
• Check browser profile paths in settings

📧 SUPPORT:
Visit wesellis.com for more information
Report issues on GitHub
        """
        
        help_textbox = ctk.CTkTextbox(help_window)
        help_textbox.pack(fill="both", expand=True, padx=20, pady=20)
        help_textbox.insert("1.0", help_text)
        help_textbox.configure(state="disabled")
        
        close_btn = ctk.CTkButton(
            help_window,
            text="Close",
            command=help_window.destroy
        )
        close_btn.pack(pady=10)
    
    def _update_status(self, message: str):
        """Update status bar message"""
        self.status_label.configure(text=message)
        logger.info(message)
    
    def _update_preview(self):
        """Update icon preview"""
        # Implementation for live preview updates
        pass
    
    def _filter_profiles(self, *args):
        """Filter profiles based on search"""
        # Implementation for profile search/filter
        pass
    
    def _get_random_color(self) -> str:
        """Get random color from palette"""
        import random
        color_info = random.choice(self.color_palette)
        return color_info['hex']
    
    def _adjust_color_brightness(self, hex_color: str, factor: float) -> str:
        """Adjust color brightness"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        r = int(min(255, r * factor))
        g = int(min(255, g * factor))
        b = int(min(255, b * factor))
        
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def _update_color_mode(self, mode):
        """Update color mode"""
        self._update_preview()
    
    def _select_color(self, color_info):
        """Select color from palette"""
        if self.selected_profile_index is not None:
            self.profiles[self.selected_profile_index]['color'] = color_info
            self._display_profiles()
    
    def _pick_custom_color(self):
        """Open custom color picker"""
        color = colorchooser.askcolor()
        if color[1] and self.selected_profile_index is not None:
            self.profiles[self.selected_profile_index]['color'] = {'hex': color[1]}
            self._display_profiles()
    
    def _set_shape(self, shape):
        """Set icon shape"""
        self.current_shape = shape
        self._update_preview()
    
    def _update_radius(self, value):
        """Update corner radius"""
        self._update_preview()
    
    def _update_font(self, font):
        """Update font family"""
        self.current_font = font
        self._update_preview()
    
    def _update_font_size(self, size):
        """Update font size"""
        self._update_preview()
    
    def _update_text_position(self, position):
        """Update text position"""
        self._update_preview()
    
    def _update_opacity(self, value):
        """Update icon opacity"""
        self._update_preview()
    
    def _clear_cache(self):
        """Clear icon cache"""
        self._image_cache.clear()
        self._icon_preview_cache.clear()
        messagebox.showinfo("Success", "Cache cleared successfully")
    
    def _export_settings(self):
        """Export application settings"""
        settings = {
            "theme": self.theme_mode,
            "shape": self.current_shape,
            "font": self.current_font,
            "show_text": self.show_text_var.get(),
            "effects": {
                "shadow": self.shadow_var.get(),
                "glow": self.glow_var.get(),
                "border": self.border_var.get()
            }
        }
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(settings, f, indent=2)
            messagebox.showinfo("Success", "Settings exported successfully")
    
    def _import_settings(self):
        """Import application settings"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    settings = json.load(f)
                
                # Apply settings
                self.theme_mode = settings.get("theme", "dark")
                self.current_shape = settings.get("shape", "rounded")
                self.current_font = settings.get("font", "Segoe UI")
                self.show_text_var.set(settings.get("show_text", True))
                
                effects = settings.get("effects", {})
                self.shadow_var.set(effects.get("shadow", True))
                self.glow_var.set(effects.get("glow", False))
                self.border_var.set(effects.get("border", False))
                
                self._update_preview()
                messagebox.showinfo("Success", "Settings imported successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import settings: {str(e)}")
    
    def _load_settings(self):
        """Load saved settings from file"""
        settings_file = "profilepop_settings.json"
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                # Apply settings
                # ... (implementation)
            except Exception as e:
                logger.error(f"Error loading settings: {e}")
    
    def _save_settings(self):
        """Save current settings to file"""
        settings_file = "profilepop_settings.json"
        settings = {
            "theme": self.theme_mode,
            "shape": self.current_shape,
            "font": self.current_font,
            # ... more settings
        }
        
        try:
            with open(settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
    
    def _start_background_tasks(self):
        """Start background tasks for performance"""
        # Auto-save timer
        self.after(60000, self._auto_save)  # Auto-save every minute
    
    def _auto_save(self):
        """Auto-save settings periodically"""
        self._save_settings()
        self.after(60000, self._auto_save)  # Schedule next save

# Import required for math functions
from math import cos, sin
from PIL import ImageEnhance

def main():
    """Main entry point"""
    app = ModernProfilePop()
    app.mainloop()

if __name__ == "__main__":
    main()