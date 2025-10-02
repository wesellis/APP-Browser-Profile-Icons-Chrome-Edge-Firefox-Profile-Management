"""
Build Web Store Submission Packages
Creates ZIP files ready for Chrome Web Store, Firefox Add-ons, and Edge Add-ons
"""

import os
import zipfile
from datetime import datetime


def create_zip(source_dir, output_file, exclude_patterns=None):
    """Create a ZIP file from directory"""
    if exclude_patterns is None:
        exclude_patterns = ['.git', '__pycache__', '.DS_Store', 'Thumbs.db', '.idea']

    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_patterns]

            for file in files:
                # Skip excluded files
                if any(pattern in file for pattern in exclude_patterns):
                    continue

                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)

    return output_file


def build_packages():
    """Build all extension packages"""
    print("🚀 Building Web Store Packages...")
    print("=" * 50)

    timestamp = datetime.now().strftime("%Y%m%d")
    output_dir = "web-store-packages"
    os.makedirs(output_dir, exist_ok=True)

    packages = [
        {
            'name': 'Chrome',
            'source': 'chrome-extension',
            'output': f'browser-profile-icons-chrome-v3.0.0-{timestamp}.zip'
        },
        {
            'name': 'Firefox',
            'source': 'firefox-extension',
            'output': f'browser-profile-icons-firefox-v3.0.0-{timestamp}.zip'
        },
        {
            'name': 'Edge',
            'source': 'edge-extension',
            'output': f'browser-profile-icons-edge-v3.0.0-{timestamp}.zip'
        }
    ]

    built_packages = []

    for package in packages:
        source_dir = package['source']
        if not os.path.exists(source_dir):
            print(f"⚠️  Skipping {package['name']}: {source_dir} not found")
            continue

        output_path = os.path.join(output_dir, package['output'])

        print(f"\n📦 Building {package['name']} extension...")
        print(f"   Source: {source_dir}")
        print(f"   Output: {output_path}")

        try:
            create_zip(source_dir, output_path)
            file_size = os.path.getsize(output_path) / 1024  # KB
            print(f"   ✅ Created: {file_size:.1f} KB")
            built_packages.append((package['name'], output_path, file_size))
        except Exception as e:
            print(f"   ❌ Error: {e}")

    print("\n" + "=" * 50)
    print("📊 Build Summary:")
    print("=" * 50)

    for name, path, size in built_packages:
        print(f"✅ {name:10} - {size:6.1f} KB - {path}")

    print(f"\n🎉 Successfully built {len(built_packages)}/{len(packages)} packages!")
    print(f"📁 Location: {os.path.abspath(output_dir)}")

    # Create submission checklist
    create_submission_checklist(output_dir)


def create_submission_checklist(output_dir):
    """Create a submission checklist"""
    checklist = """
# Web Store Submission Checklist

## Before Submission

### All Stores
- [ ] Test extension in target browser
- [ ] Verify all permissions are necessary
- [ ] Update version number in manifest.json
- [ ] Create icon assets (16x16, 32x32, 48x48, 128x128)
- [ ] Write clear description
- [ ] Take screenshots (1280x800 or 640x400)
- [ ] Create promotional images if required

### Chrome Web Store
- [ ] Developer account ($5 one-time fee)
- [ ] Privacy policy URL (if using permissions)
- [ ] Store listing description (min 132 characters)
- [ ] Screenshots (1280x800 or 640x400, max 5)
- [ ] Small tile icon (440x280)

### Firefox Add-ons
- [ ] Firefox Developer account (free)
- [ ] Add-on description
- [ ] Screenshots (max 10)
- [ ] Support email or URL
- [ ] Privacy policy (recommended)

### Microsoft Edge Add-ons
- [ ] Microsoft Partner Center account
- [ ] Store listing description
- [ ] Screenshots (1280x800 or 640x400)
- [ ] Support email
- [ ] Privacy policy URL

## Submission URLs

- Chrome: https://chrome.google.com/webstore/devconsole
- Firefox: https://addons.mozilla.org/developers/
- Edge: https://partner.microsoft.com/dashboard/microsoftedge

## Testing Before Upload

1. Load unpacked extension in developer mode
2. Test all features:
   - [ ] Profile creation
   - [ ] Profile switching
   - [ ] Keyboard shortcuts
   - [ ] Export/Import
   - [ ] Search functionality
   - [ ] Template gallery
3. Check for errors in console
4. Test on clean browser profile

## After Submission

- [ ] Monitor review status
- [ ] Respond to any reviewer feedback
- [ ] Update README with store links once approved
- [ ] Promote on social media/GitHub

## Version History

- v3.0.0 - Initial major release
  - 59+ icon templates
  - Search and filter
  - Template gallery
  - Export/Import
  - Keyboard shortcuts
"""

    checklist_path = os.path.join(output_dir, "SUBMISSION_CHECKLIST.md")
    with open(checklist_path, 'w') as f:
        f.write(checklist.strip())

    print(f"\n📋 Submission checklist created: {checklist_path}")


if __name__ == "__main__":
    build_packages()
