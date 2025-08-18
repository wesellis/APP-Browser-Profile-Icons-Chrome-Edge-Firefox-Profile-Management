#!/usr/bin/env python3
"""Generate Chrome Web Store assets for Browser Profile Icons"""

import os

# Create assets directory
assets_dir = 'chrome_store_assets'
os.makedirs(assets_dir, exist_ok=True)

# Store listing content
store_listing = """
STORE LISTING CONTENT FOR CHROME WEB STORE
==========================================

NAME: Browser Profile Icons Pro

SHORT DESCRIPTION (132 chars max):
Manage browser profiles with custom icons, quick switching, and cloud sync. Keep work and personal browsing separate!

DETAILED DESCRIPTION:
Browser Profile Icons Pro is the ultimate solution for managing multiple browser profiles with ease. Whether you're juggling work and personal browsing, managing multiple client projects, or simply want better organization, this extension has you covered.

✨ KEY FEATURES:
• Create unlimited browser profiles (Free: 5 profiles)
• Custom colors and icons for each profile
• One-click profile switching
• Keyboard shortcuts for instant switching (Ctrl+Shift+1-9)
• Cloud sync across devices (Pro)
• Auto-switch profiles based on websites (Pro)
• Import/Export profiles for backup
• Privacy-focused - keep browsing data separate

🎯 PERFECT FOR:
• Remote workers managing multiple clients
• Developers testing with different accounts
• Social media managers
• Anyone who values privacy and organization

💎 FREE VERSION INCLUDES:
• Up to 5 profiles
• Basic profile switching
• Custom colors
• One keyboard shortcut

⭐ PRO VERSION ($4.99 one-time):
• Unlimited profiles
• All keyboard shortcuts
• Cloud sync
• Custom icons
• Import/Export
• Auto-switching rules
• Priority support
• Lifetime updates

🔒 PRIVACY FIRST:
• No data collection
• All data stored locally
• Cloud sync is optional and encrypted
• Open source on GitHub

🚀 GETTING STARTED:
1. Click the extension icon
2. Create your first profile
3. Switch between profiles instantly
4. Use Ctrl+Shift+1 for quick access

💬 SUPPORT:
• Email: support@browserprofileicons.com
• GitHub: https://github.com/wesellis/browser-profile-icons

Try the 7-day free trial of Pro features - no credit card required!

---
Version 2.0 - Major update with cloud sync, keyboard shortcuts, and improved UI
"""

# Save store listing
with open(os.path.join(assets_dir, 'store_listing.txt'), 'w') as f:
    f.write(store_listing)

# Screenshot descriptions
screenshots = """
SCREENSHOT DESCRIPTIONS
=======================

1. screenshot_1_main.png (1280x800)
   - Show the main popup with several colorful profiles
   - Highlight the clean, modern interface
   - Show both free and pro badges

2. screenshot_2_switching.png (1280x800)
   - Demonstrate profile switching in action
   - Show the visual feedback when switching
   - Include keyboard shortcut hint

3. screenshot_3_options.png (1280x800)
   - Show the options page with profile management
   - Display the profile grid with editing capabilities
   - Show pro features clearly marked

4. screenshot_4_features.png (1280x800)
   - Feature comparison table
   - Highlight the benefits of Pro version
   - Show the one-time pricing

5. screenshot_5_welcome.png (1280x800)
   - Welcome page after installation
   - Show the 7-day trial notice
   - List key features with icons
"""

with open(os.path.join(assets_dir, 'screenshot_descriptions.txt'), 'w') as f:
    f.write(screenshots)

# Promotional images
promo_text = """
PROMOTIONAL IMAGES NEEDED
========================

1. Small Promo Tile (440x280)
   - Extension icon prominently displayed
   - Tagline: "Smart Browser Profile Management"
   - Show 3-4 colorful profile icons
   - "$4.99 Pro Version" badge

2. Large Promo Tile (920x680) - Optional
   - Hero image showing multiple profiles
   - Feature list on the side
   - Professional, clean design
   - Call-to-action: "Try 7-Day Free Trial"

3. Marquee Promo (1400x560) - Optional
   - Wide banner showcasing the extension
   - Before/after comparison
   - "Organize Your Digital Life" message
"""

with open(os.path.join(assets_dir, 'promo_images.txt'), 'w') as f:
    f.write(promo_text)

# Icon specifications
icon_specs = """
ICON CREATION GUIDE
==================

Create these icon files in chrome-extension/images/:

1. icon16.png (16x16)
2. icon48.png (48x48)
3. icon128.png (128x128)

Design suggestions:
- Use a grid of 4 colored squares/circles
- Each square represents a profile
- Use vibrant colors: blue, green, orange, purple
- Add subtle shadow for depth
- Keep it simple and recognizable at small sizes

Store Icon (128x128):
- Same design but with more polish
- Add subtle gradient
- Ensure it stands out in the Chrome Web Store
"""

with open(os.path.join(assets_dir, 'icon_specifications.txt'), 'w') as f:
    f.write(icon_specs)

# Create placeholder icon (simple SVG)
svg_icon = """<svg width="128" height="128" xmlns="http://www.w3.org/2000/svg">
  <rect width="128" height="128" fill="#f5f5f5" rx="16"/>
  
  <!-- Top-left profile -->
  <circle cx="40" cy="40" r="24" fill="#4285f4"/>
  <text x="40" y="48" text-anchor="middle" fill="white" font-size="24" font-weight="bold">W</text>
  
  <!-- Top-right profile -->
  <circle cx="88" cy="40" r="24" fill="#34a853"/>
  <text x="88" y="48" text-anchor="middle" fill="white" font-size="24" font-weight="bold">P</text>
  
  <!-- Bottom-left profile -->
  <circle cx="40" cy="88" r="24" fill="#fbbc04"/>
  <text x="40" y="96" text-anchor="middle" fill="white" font-size="24" font-weight="bold">D</text>
  
  <!-- Bottom-right profile -->
  <circle cx="88" cy="88" r="24" fill="#ea4335"/>
  <text x="88" y="96" text-anchor="middle" fill="white" font-size="24" font-weight="bold">S</text>
</svg>"""

with open(os.path.join('chrome-extension', 'images', 'icon128.svg'), 'w') as f:
    f.write(svg_icon)

print("✅ Chrome Web Store assets created!")
print("\n📁 Files created:")
print("  - chrome_store_assets/store_listing.txt")
print("  - chrome_store_assets/screenshot_descriptions.txt")
print("  - chrome_store_assets/promo_images.txt")
print("  - chrome_store_assets/icon_specifications.txt")
print("  - chrome-extension/images/icon128.svg (placeholder)")
print("\n📸 Next steps:")
print("1. Create actual PNG icons from the SVG template")
print("2. Take screenshots as described")
print("3. Create promotional images")
print("4. Package extension as ZIP for upload")