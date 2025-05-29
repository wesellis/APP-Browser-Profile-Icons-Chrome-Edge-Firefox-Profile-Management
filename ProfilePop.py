import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from PIL import Image, ImageDraw
import threading
import subprocess
import configparser

# Version info
__version__ = "1.2.0"
__app_name__ = "ProfilePop"
__description__ = "Browser Profile Icon Generator"

class ProfilePop:
    def __init__(self, root):
        self.root = root
        self.edge_data_path = os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data")
        self.firefox_data_path = os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox")
        self.chrome_data_path = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data")
        
        self.profiles = []
        self.profile_colors = {}
        self.current_browser = None
        
        # Your custom color palette - organized dark to light (white to black)
        self.color_palette = [
            '#10121c', '#2c1e31', '#6b2643', '#ac2847', '#ec273f',
            '#94493a', '#de5d3a', '#e98537', '#f3a833', '#4d3533',
            '#6e4c30', '#a26d3f', '#ce9248', '#dab163', '#e8d282',
            '#f7f3b7', '#1e4044', '#006554', '#26854c', '#5ab552',
            '#9de64e', '#008b8b', '#62a477', '#a6cb96', '#d3eed3',
            '#3e3b65', '#3859b3', '#3388de', '#36c5f4', '#6dead6',
            '#5e5b8c', '#8c78a5', '#b0a7b8', '#deceed', '#9a4d76',
            '#c878af', '#cc99ff', '#fa6e79', '#ffa2ac', '#ffd1d5',
            '#f6e8e0', '#ffffff'
        ]
        
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title(f"{__app_name__} v{__version__} - {__description__}")
        self.root.geometry("900x650")
        self.root.configure(bg='#2f3136')  # Discord dark background
        
        # Dark Discord-style header
        header_canvas = tk.Canvas(self.root, height=70, highlightthickness=0, bg='#202225')
        header_canvas.pack(fill='x')
        
        # Darker gradient colors for Discord theme
        gradient_colors = ['#5865f2', '#4752c4', '#3c4590', '#32385c', '#282b30']
        for i, color in enumerate(gradient_colors):
            x1 = i * 180
            x2 = (i + 2) * 180
            header_canvas.create_rectangle(x1, 0, x2, 70, fill=color, outline='')
        
        header_canvas.create_text(450, 35, text=f"{__app_name__} v{__version__}", font=('Segoe UI', 22, 'bold'), fill='white')
        
        # Main content with Discord dark theme
        main_frame = tk.Frame(self.root, bg='#2f3136')
        main_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Top section - Description on left, buttons on right
        top_section = tk.Frame(main_frame, bg='#2f3136')
        top_section.pack(fill='x', pady=(0, 20))
        
        # Left side - Description
        desc_frame = tk.Frame(top_section, bg='#2f3136')
        desc_frame.pack(side='left', fill='both', expand=True)
        
        desc_label = tk.Label(desc_frame, text="Generate custom icons for Edge, Firefox, and Chrome profiles\nIcons are stored in AppData\\Local\\ProfilePop for permanence", 
                             font=('Segoe UI', 12), bg='#2f3136', fg='#dcddde', anchor='w', justify='left')
        desc_label.pack(anchor='w')
        
        # Right side - Action buttons
        button_frame = tk.Frame(top_section, bg='#2f3136')
        button_frame.pack(side='right', padx=(20, 0))
        
        # Discord-style buttons
        tk.Button(button_frame, text="Generate Icons", font=('Segoe UI', 10, 'bold'),
                 bg='#5865f2', fg='white', relief='flat', padx=15, pady=8,
                 activebackground='#4752c4', activeforeground='white',
                 command=self.generate_icons).pack(side='left', padx=(0, 8))
        
        tk.Button(button_frame, text="Create Shortcuts", font=('Segoe UI', 10, 'bold'),
                 bg='#57f287', fg='#2f3136', relief='flat', padx=15, pady=8,
                 activebackground='#43b581', activeforeground='#2f3136',
                 command=self.create_shortcuts).pack(side='left', padx=(0, 8))
        
        tk.Button(button_frame, text="Open Folder", font=('Segoe UI', 10, 'bold'),
                 bg='#36393f', fg='#dcddde', relief='flat', padx=15, pady=8,
                 activebackground='#40444b', activeforeground='white',
                 command=self.open_folder).pack(side='left')
        
        # Status section
        status_frame = tk.Frame(main_frame, bg='#36393f', relief='flat', bd=1)
        status_frame.pack(fill='x', pady=(0, 15))
        
        self.status_label = tk.Label(status_frame, text="Select a browser to view profiles", 
                                    font=('Segoe UI', 10), bg='#36393f', fg='#b9bbbe', pady=8, padx=12)
        self.status_label.pack(anchor='w')
        
        # Profiles section with browser buttons on the left
        profiles_section = tk.Frame(main_frame, bg='#2f3136')
        profiles_section.pack(fill='x', pady=(0, 15))
        
        # Browser selection buttons (left side)
        browser_frame = tk.Frame(profiles_section, bg='#2f3136')
        browser_frame.pack(side='left', fill='y', padx=(0, 15))
        
        browser_label = tk.Label(browser_frame, text="Select Browser:", font=('Segoe UI', 10, 'bold'), 
                                bg='#2f3136', fg='#ffffff')
        browser_label.pack(anchor='w', pady=(0, 8))
        
        # Edge button
        edge_btn = tk.Button(browser_frame, text="EDGE", font=('Segoe UI', 9, 'bold'),
                           bg='#0078d4', fg='white', relief='flat', padx=12, pady=6,
                           activebackground='#106ebe', activeforeground='white',
                           command=lambda: self.load_browser_profiles('edge'))
        edge_btn.pack(fill='x', pady=(0, 5))
        
        # Firefox button
        firefox_btn = tk.Button(browser_frame, text="FIREFOX", font=('Segoe UI', 9, 'bold'),
                              bg='#ff9500', fg='white', relief='flat', padx=12, pady=6,
                              activebackground='#e8890b', activeforeground='white',
                              command=lambda: self.load_browser_profiles('firefox'))
        firefox_btn.pack(fill='x', pady=(0, 5))
        
        # Chrome button
        chrome_btn = tk.Button(browser_frame, text="CHROME", font=('Segoe UI', 9, 'bold'),
                             bg='#34a853', fg='white', relief='flat', padx=12, pady=6,
                             activebackground='#2d8f47', activeforeground='white',
                             command=lambda: self.load_browser_profiles('chrome'))
        chrome_btn.pack(fill='x')
        
        # Profiles table (right side)
        profiles_frame = tk.Frame(profiles_section, bg='#2f3136')
        profiles_frame.pack(side='left', fill='both', expand=True)
        
        profiles_label = tk.Label(profiles_frame, text="Browser Profiles", font=('Segoe UI', 12, 'bold'), 
                                 bg='#2f3136', fg='#ffffff', anchor='w')
        profiles_label.pack(anchor='w', pady=(0, 8))
        
        # Dark-themed treeview
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview",
                       background="#40444b",
                       foreground="#dcddde",
                       rowheight=25,
                       fieldbackground="#40444b",
                       borderwidth=0,
                       relief="flat")
        style.configure("Treeview.Heading",
                       background="#36393f",
                       foreground="#ffffff",
                       relief="flat",
                       borderwidth=1)
        style.map("Treeview", background=[('selected', '#5865f2')])
        
        self.profile_tree = ttk.Treeview(profiles_frame, columns=('Name', 'Color'), show='headings', height=6)
        self.profile_tree.heading('Name', text='Profile Name')
        self.profile_tree.heading('Color', text='Color')
        self.profile_tree.column('Name', width=300)
        self.profile_tree.column('Color', width=150)
        self.profile_tree.pack(fill='x', pady=(0, 15))
        self.profile_tree.bind('<Double-1>', self.on_profile_select)
        
        # Color palette section
        palette_label = tk.Label(main_frame, text="Double-click a profile above, then click a color:", 
                                font=('Segoe UI', 10), bg='#2f3136', fg='#b9bbbe')
        palette_label.pack(anchor='w', pady=(0, 8))
        
        # Color palette with dark theme
        colors_frame = tk.Frame(main_frame, bg='#36393f', relief='flat', bd=1)
        colors_frame.pack(fill='x', pady=(0, 15))
        
        colors_inner = tk.Frame(colors_frame, bg='#36393f')
        colors_inner.pack(pady=8, padx=8)
        
        for i, color in enumerate(self.color_palette):
            color_btn = tk.Button(colors_inner, bg=color, width=2, height=7,
                                relief='flat', bd=0, cursor='hand2',
                                activebackground=color,
                                command=lambda c=color: self.select_color(c))
            color_btn.grid(row=0, column=i, padx=1, pady=0)
        
        # Selection info
        self.selection_info = tk.Label(main_frame, text="Select a browser and profile to get started", 
                                      font=('Segoe UI', 9), bg='#2f3136', fg='#72767d')
        self.selection_info.pack(anchor='w')
        
        self.selected_profile_item = None
        
    def load_browser_profiles(self, browser):
        self.current_browser = browser
        self.status_label.config(text=f"Scanning for {browser.title()} profiles...", fg='#faa61a')
        threading.Thread(target=self._scan_browser_profiles_thread, args=(browser,), daemon=True).start()
        
    def _scan_browser_profiles_thread(self, browser):
        try:
            if browser == 'edge':
                self.profiles = self.get_edge_profiles()
            elif browser == 'firefox':
                self.profiles = self.get_firefox_profiles()
            elif browser == 'chrome':
                self.profiles = self.get_chrome_profiles()
            else:
                self.profiles = []
                
            self.root.after(0, self._update_profiles_display)
        except Exception as e:
            # Show error in status bar instead of popup
            error_msg = f"{browser.title()} not found or no profiles available"
            self.root.after(0, lambda: self.status_label.config(text=error_msg, fg='#ff6b6b'))
            
    def _update_profiles_display(self):
        # Clear existing profiles
        for item in self.profile_tree.get_children():
            self.profile_tree.delete(item)
            
        # Add new profiles
        for profile in self.profiles:
            display_color = self.profile_colors.get(profile['name'], profile['theme_color'])
            self.profile_tree.insert('', 'end', values=(profile['name'], display_color))
            
        browser_name = self.current_browser.title() if self.current_browser else "Browser"
        self.status_label.config(text=f"Found {len(self.profiles)} {browser_name} profiles - Ready to generate icons", fg='#43b581')
        
    def get_edge_profiles(self):
        profiles = []
        try:
            local_state_path = os.path.join(self.edge_data_path, "Local State")
            if not os.path.exists(local_state_path):
                raise Exception("Edge data not found")
                
            with open(local_state_path, 'r', encoding='utf-8') as f:
                local_state = json.load(f)
                
            profile_info = local_state.get('profile', {}).get('info_cache', {})
            
            colors = ['#5865f2', '#57f287', '#feb47b', '#ff7eb9', '#c44569', '#f8b500']
            for i, (profile_id, profile_data) in enumerate(profile_info.items()):
                name = profile_data.get('name', profile_id)
                theme_color = colors[i % len(colors)]
                
                profiles.append({
                    'id': profile_id,
                    'name': f"{name} - EDGE",
                    'original_name': name,
                    'theme_color': theme_color,
                    'browser': 'edge'
                })
                
        except Exception as e:
            raise Exception(f"Failed to read Edge profiles: {str(e)}")
            
        return profiles
    
    def get_firefox_profiles(self):
        profiles = []
        try:
            profiles_ini_path = os.path.join(self.firefox_data_path, "profiles.ini")
            if not os.path.exists(profiles_ini_path):
                raise Exception("Firefox profiles.ini not found")
            
            config = configparser.ConfigParser()
            config.read(profiles_ini_path, encoding='utf-8')
            
            colors = ['#ff9500', '#57f287', '#feb47b', '#ff7eb9', '#c44569', '#f8b500']
            profile_count = 0
            
            for section_name in config.sections():
                if section_name.startswith('Profile'):
                    profile_data = config[section_name]
                    name = profile_data.get('Name', f'Profile {profile_count}')
                    path = profile_data.get('Path', '')
                    
                    theme_color = colors[profile_count % len(colors)]
                    
                    profiles.append({
                        'id': path,
                        'name': f"{name} - FIREFOX",
                        'original_name': name,
                        'theme_color': theme_color,
                        'browser': 'firefox'
                    })
                    profile_count += 1
                    
        except Exception as e:
            raise Exception(f"Failed to read Firefox profiles: {str(e)}")
            
        return profiles
    
    def get_chrome_profiles(self):
        profiles = []
        try:
            local_state_path = os.path.join(self.chrome_data_path, "Local State")
            if not os.path.exists(local_state_path):
                raise Exception("Chrome data not found")
                
            with open(local_state_path, 'r', encoding='utf-8') as f:
                local_state = json.load(f)
                
            profile_info = local_state.get('profile', {}).get('info_cache', {})
            
            colors = ['#4285f4', '#57f287', '#feb47b', '#ff7eb9', '#c44569', '#f8b500']
            for i, (profile_id, profile_data) in enumerate(profile_info.items()):
                name = profile_data.get('name', profile_id)
                theme_color = colors[i % len(colors)]
                
                profiles.append({
                    'id': profile_id,
                    'name': f"{name} - CHROME",
                    'original_name': name,
                    'theme_color': theme_color,
                    'browser': 'chrome'
                })
                
        except Exception as e:
            raise Exception(f"Failed to read Chrome profiles: {str(e)}")
            
        return profiles
    
    def on_profile_select(self, event):
        selection = self.profile_tree.selection()
        if selection:
            self.selected_profile_item = selection[0]
            profile_name = self.profile_tree.item(self.selected_profile_item)['values'][0]
            self.selection_info.config(text=f"Selected: {profile_name} - Click a color to change", fg='#dcddde')
            
    def select_color(self, color):
        if self.selected_profile_item:
            profile_name = self.profile_tree.item(self.selected_profile_item)['values'][0]
            self.profile_colors[profile_name] = color
            current_values = list(self.profile_tree.item(self.selected_profile_item)['values'])
            current_values[1] = color
            self.profile_tree.item(self.selected_profile_item, values=current_values)
            self.selection_info.config(text=f"Color updated for {profile_name}", fg='#43b581')
            self.root.after(3000, lambda: self.selection_info.config(text="Select a profile to change its color", fg='#72767d'))
        else:
            messagebox.showinfo("No Selection", "Please double-click on a profile first.")
    
    def sanitize_filename(self, filename):
        clean_name = filename.replace(' ', '_').replace(':', '').replace('/', '_')
        clean_name = clean_name.replace('\\', '_').replace('?', '').replace('*', '')
        clean_name = clean_name.replace('<', '').replace('>', '').replace('|', '').replace('"', '')
        return clean_name
    
    def generate_icons(self):
        if not self.profiles:
            messagebox.showwarning("No Profiles", "Please select a browser and load profiles first.")
            return
            
        self.status_label.config(text="Generating icons...", fg='#faa61a')
        threading.Thread(target=self._generate_icons_thread, daemon=True).start()
        
    def _generate_icons_thread(self):
        try:
            # Use AppData instead of Downloads for permanent storage
            appdata_path = os.path.expanduser("~\AppData\Local\ProfilePop")
            icons_folder = os.path.join(appdata_path, "icons")
            
            # Try to clear the icons folder
            import shutil
            if os.path.exists(icons_folder):
                try:
                    # Delete individual files instead of the whole folder
                    for filename in os.listdir(icons_folder):
                        if filename.endswith('.ico'):
                            file_path = os.path.join(icons_folder, filename)
                            os.remove(file_path)
                            print(f"🗑️ Deleted old icon: {filename}")
                except Exception as e:
                    print(f"⚠️ Could not delete some files: {e}")
            
            # Ensure folder exists
            os.makedirs(icons_folder, exist_ok=True)
            print(f"📁 Icons folder ready: {icons_folder}")
            
            # Wait a moment for filesystem
            import time
            time.sleep(1)
            
            # Generate each icon with unique names including browser and timestamp
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            for profile in self.profiles:
                print(f"\n🎯 GENERATING: {profile['name']}")
                self.create_browser_logo_icon(profile, icons_folder, timestamp)
                
            # Clear Windows icon cache to force refresh
            try:
                import subprocess
                subprocess.run(['ie4uinit.exe', '-show'], shell=True, capture_output=True)
                print("🔄 Refreshed Windows icon cache")
            except:
                print("⚠️ Could not refresh icon cache")
                
            self.root.after(0, self._generation_complete)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error generating icons: {str(e)}"))
            
    def create_browser_logo_icon(self, profile, output_folder, timestamp=""):
        """Creates icons with ONLY browser logos - ZERO text generation"""
        print(f"🎨 Creating logo icon for: {profile['name']}")
        
        # Icon setup
        size = 256
        img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
        
        # Get background color
        color_to_use = self.profile_colors.get(profile['name'], profile['theme_color'])
        if isinstance(color_to_use, str) and color_to_use.startswith('#'):
            bg_color = tuple(int(color_to_use[i:i+2], 16) for i in (1, 3, 5))
        else:
            bg_color = (88, 101, 242)  # Default blue
            
        print(f"🎨 Background color: {bg_color}")
        
        # Draw rounded rectangle background
        draw = ImageDraw.Draw(img)
        margin = 20
        corner_radius = 30
        
        # Helper function for rounded rectangle
        def rounded_rectangle(x1, y1, x2, y2, radius, fill):
            draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
            draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
            draw.pieslice([x1, y1, x1 + 2*radius, y1 + 2*radius], 180, 270, fill=fill)
            draw.pieslice([x2 - 2*radius, y1, x2, y1 + 2*radius], 270, 360, fill=fill)
            draw.pieslice([x1, y2 - 2*radius, x1 + 2*radius, y2], 90, 180, fill=fill)
            draw.pieslice([x2 - 2*radius, y2 - 2*radius, x2, y2], 0, 90, fill=fill)
        
        # Draw colored background
        rounded_rectangle(margin, margin, size-margin, size-margin, corner_radius, bg_color)
        print("✅ Drew background")
        
        # Load browser logo
        browser_logos = {
            'edge': 'microsoft-edge-browser-logo-blue-green-gradient-icon.png',
            'firefox': 'firefox-browser-logo-red-yellow-blue-circle-icon.png',
            'chrome': 'google-chrome-logo-main-icon.png'
        }
        
        browser = profile['browser']
        logo_file = browser_logos.get(browser)
        
        if logo_file:
            logo_path = os.path.join(os.path.expanduser("~"), "Downloads", "ProfilePop", "logos", logo_file)
            print(f"🔍 Looking for: {logo_path}")
            
            if os.path.exists(logo_path):
                try:
                    # Load and process logo
                    logo = Image.open(logo_path).convert('RGBA')
                    print(f"📥 Loaded logo: {logo.size}")
                    
                    # Calculate size (75% of available space - larger than before)
                    available_size = size - (2 * margin)
                    target_size = int(available_size * 0.75)
                    
                    # Resize logo proportionally
                    logo.thumbnail((target_size, target_size), Image.Resampling.LANCZOS)
                    final_size = logo.size
                    print(f"📏 Resized to: {final_size}")
                    
                    # Position logo in upper portion (move up from center)
                    logo_x = (size - final_size[0]) // 2
                    logo_y = margin + int((available_size - final_size[1]) * 0.25)  # 25% from top instead of center
                    
                    # Paste the logo (no shadow)
                    img.paste(logo, (logo_x, logo_y), logo)
                    print(f"✅ Pasted {browser} logo at ({logo_x}, {logo_y})")
                    
                    # Add profile name below the logo
                    profile_name = profile['original_name']
                    
                    # Calculate text color based on background brightness
                    brightness = (bg_color[0] * 0.299 + bg_color[1] * 0.587 + bg_color[2] * 0.114)
                    text_color = (255, 255, 255) if brightness < 127 else (0, 0, 0)  # White for dark, black for light
                    
                    # Add text below logo
                    try:
                        from PIL import ImageFont
                        # Try to use a nice font
                        font_size = 20
                        try:
                            font = ImageFont.truetype("arial.ttf", font_size)
                        except:
                            try:
                                font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
                            except:
                                try:
                                    font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", font_size)
                                except:
                                    font = ImageFont.load_default()
                        
                        # Get text dimensions
                        bbox = draw.textbbox((0, 0), profile_name, font=font)
                        text_width = bbox[2] - bbox[0]
                        text_height = bbox[3] - bbox[1]
                        
                        # Position text below logo, centered
                        text_x = (size - text_width) // 2
                        text_y = logo_y + final_size[1] + 20  # 20px gap below logo
                        
                        # Draw text
                        draw.text((text_x, text_y), profile_name, fill=text_color, font=font)
                        print(f"✅ Added text '{profile_name}' at ({text_x}, {text_y}) in {'white' if brightness < 127 else 'black'}")
                        
                    except Exception as text_error:
                        print(f"⚠️ Could not add text: {text_error}")
                    
                except Exception as e:
                    print(f"❌ Logo error: {e}")
            else:
                print(f"❌ Logo not found: {logo_path}")
        else:
            print(f"❌ No logo mapped for browser: {browser}")
        
        # Save icon file with browser name and timestamp for OneDrive compatibility
        clean_name = self.sanitize_filename(profile['original_name'])
        browser_name = profile['browser'].upper()
        if timestamp:
            icon_filename = f"{clean_name}_{browser_name}_{timestamp}.ico"
        else:
            icon_filename = f"{clean_name}_{browser_name}.ico"
        icon_path = os.path.join(output_folder, icon_filename)
        
        # Create multi-size ICO with proper taskbar sizing
        sizes = [(16, 16), (20, 20), (24, 24), (32, 32), (40, 40), (48, 48), (64, 64), (96, 96), (128, 128), (256, 256)]
        icons = []
        for target_size in sizes:
            if target_size == (256, 256):
                icons.append(img)
            else:
                # Use high-quality resampling for all sizes
                resized = img.resize(target_size, Image.Resampling.LANCZOS)
                icons.append(resized)
        
        img.save(icon_path, format='ICO', sizes=[(icon.width, icon.height) for icon in icons])
        print(f"💾 Saved: {icon_filename}")
        
        return icon_path
    
    def _generation_complete(self):
        self.status_label.config(text="Icons generated successfully!", fg='#43b581')
        # No popup - just status message
        
    def create_shortcuts(self):
        if not self.profiles:
            messagebox.showwarning("No Profiles", "Please select a browser and load profiles first.")
            return
            
        self.status_label.config(text="Creating shortcuts...", fg='#faa61a')
        threading.Thread(target=self._create_shortcuts_thread, daemon=True).start()
        
    def _create_shortcuts_thread(self):
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop_path = winshell.desktop()
            # Use AppData for permanent icon storage
            appdata_path = os.path.expanduser("~\AppData\Local\ProfilePop")
            icons_folder = os.path.join(appdata_path, "icons")
            
            # Browser executable paths
            browser_paths = {
                'edge': [
                    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
                    "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe"
                ],
                'firefox': [
                    "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
                    "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"
                ],
                'chrome': [
                    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
                ]
            }
            
            shortcuts_created = 0
            
            for profile in self.profiles:
                try:
                    browser = profile['browser']
                    
                    # Find the correct executable path
                    exe_path = None
                    for path in browser_paths[browser]:
                        if os.path.exists(path):
                            exe_path = path
                            break
                    
                    if not exe_path:
                        print(f"✗ {browser.title()} executable not found for {profile['name']}")
                        continue
                    
                    shell = Dispatch('WScript.Shell')
                    shortcut_name = f"{profile['name']}.lnk"
                    shortcut_path = os.path.join(desktop_path, shortcut_name)
                    shortcut = shell.CreateShortCut(shortcut_path)
                    
                    shortcut.Targetpath = exe_path
                    
                    # Set browser-specific arguments
                    if browser == 'edge':
                        shortcut.Arguments = f'--profile-directory="{profile["id"]}"'
                    elif browser == 'firefox':
                        shortcut.Arguments = f'-P "{profile["original_name"]}"'
                    elif browser == 'chrome':
                        shortcut.Arguments = f'--profile-directory="{profile["id"]}"'
                    
                    shortcut.WorkingDirectory = os.path.dirname(exe_path)
                    
                    # Set icon - look for timestamped file with browser name
                    clean_name = self.sanitize_filename(profile['original_name'])
                    browser_name = profile['browser'].upper()
                    
                    # Look for the most recent icon file for this profile and browser
                    icon_path = None
                    for filename in os.listdir(icons_folder):
                        if filename.startswith(f"{clean_name}_{browser_name}_") and filename.endswith('.ico'):
                            icon_path = os.path.join(icons_folder, filename)
                            break
                    
                    # Fallback to non-timestamped name
                    if not icon_path:
                        fallback_path = os.path.join(icons_folder, f"{clean_name}_{browser_name}.ico")
                        if os.path.exists(fallback_path):
                            icon_path = fallback_path
                    
                    if icon_path and os.path.exists(icon_path):
                        shortcut.IconLocation = f"{icon_path},0"
                        print(f"✓ Shortcut uses icon: {os.path.basename(icon_path)}")
                    
                    shortcut.save()
                    shortcuts_created += 1
                    
                except Exception as e:
                    print(f"Error creating shortcut for {profile['name']}: {e}")
                    continue
            
            self.root.after(0, lambda: self._shortcuts_complete(shortcuts_created))
            
        except ImportError:
            self.root.after(0, lambda: messagebox.showerror("Error", "Missing dependencies. Run: pip install winshell pywin32"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error creating shortcuts: {str(e)}"))
    
    def _shortcuts_complete(self, count):
        self.status_label.config(text=f"Created {count} shortcuts successfully!", fg='#43b581')
        # No popup - just status message
        
    def open_folder(self):
        # Open AppData icons folder instead of Downloads
        appdata_path = os.path.expanduser("~\AppData\Local\ProfilePop")
        icons_folder = os.path.join(appdata_path, "icons")
        try:
            os.startfile(icons_folder)
        except:
            subprocess.run(['explorer', icons_folder], shell=True)

def main():
    root = tk.Tk()
    app = ProfilePop(root)
    root.mainloop()

if __name__ == "__main__":
    main()
