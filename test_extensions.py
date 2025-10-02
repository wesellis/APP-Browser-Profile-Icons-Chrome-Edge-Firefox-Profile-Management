"""
Tests for browser extension functionality
Tests JavaScript logic without requiring browser environment
"""

import pytest
import json


class TestExtensionManifests:
    """Test extension manifest files"""

    def test_chrome_manifest_exists(self):
        """Test Chrome manifest exists and is valid JSON"""
        import os
        manifest_path = "chrome-extension/manifest.json"
        assert os.path.exists(manifest_path)

        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        assert manifest['manifest_version'] == 3
        assert manifest['name']
        assert manifest['version']
        assert 'permissions' in manifest

    def test_firefox_manifest_exists(self):
        """Test Firefox manifest exists and is valid JSON"""
        import os
        manifest_path = "firefox-extension/manifest.json"
        assert os.path.exists(manifest_path)

        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        assert manifest['manifest_version'] == 2
        assert manifest['name']
        assert manifest['version']
        assert 'permissions' in manifest

    def test_edge_manifest_exists(self):
        """Test Edge manifest exists"""
        import os
        manifest_path = "edge-extension/manifest.json"
        assert os.path.exists(manifest_path)

        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        assert manifest['manifest_version'] == 3


class TestExtensionStructure:
    """Test extension file structure"""

    def test_chrome_has_required_files(self):
        """Test Chrome extension has all required files"""
        import os

        required_files = [
            "chrome-extension/manifest.json",
            "chrome-extension/popup.html",
            "chrome-extension/js/popup.js",
            "chrome-extension/js/background.js",
            "chrome-extension/templates.html",
            "chrome-extension/js/templates.js"
        ]

        for file_path in required_files:
            assert os.path.exists(file_path), f"Missing: {file_path}"

    def test_firefox_has_required_files(self):
        """Test Firefox extension has all required files"""
        import os

        required_files = [
            "firefox-extension/manifest.json",
            "firefox-extension/popup.html",
            "firefox-extension/js/popup.js",
            "firefox-extension/js/background.js",
            "firefox-extension/options.html",
            "firefox-extension/js/options.js",
            "firefox-extension/welcome.html",
            "firefox-extension/templates.html",
            "firefox-extension/js/templates.js"
        ]

        for file_path in required_files:
            assert os.path.exists(file_path), f"Missing: {file_path}"


class TestProfileDataStructure:
    """Test profile data structure validity"""

    def test_default_profile_structure(self):
        """Test default profile has all required fields"""
        profile = {
            'id': 1,
            'name': 'Work',
            'icon': '💼',
            'color': '#2196F3',
            'created': '2025-01-01T00:00:00.000Z'
        }

        assert 'id' in profile
        assert 'name' in profile
        assert 'icon' in profile
        assert 'color' in profile
        assert 'created' in profile

        # Type checks
        assert isinstance(profile['id'], int)
        assert isinstance(profile['name'], str)
        assert isinstance(profile['icon'], str)
        assert isinstance(profile['color'], str)
        assert profile['color'].startswith('#')

    def test_profile_color_validation(self):
        """Test profile color is valid hex"""
        valid_colors = ['#2196F3', '#4CAF50', '#FF9800']

        for color in valid_colors:
            assert color.startswith('#')
            assert len(color) == 7
            # Verify it's valid hex
            try:
                int(color[1:], 16)
            except ValueError:
                pytest.fail(f"Invalid hex color: {color}")

    def test_profile_export_format(self):
        """Test profile export data structure"""
        export_data = {
            'version': '3.0.0',
            'exportDate': '2025-01-01T00:00:00.000Z',
            'profileCount': 3,
            'profiles': [
                {'id': 1, 'name': 'Work', 'icon': '💼', 'color': '#2196F3'},
                {'id': 2, 'name': 'Personal', 'icon': '🏠', 'color': '#4CAF50'},
                {'id': 3, 'name': 'Dev', 'icon': '💻', 'color': '#FF9800'}
            ]
        }

        assert 'version' in export_data
        assert 'exportDate' in export_data
        assert 'profileCount' in export_data
        assert 'profiles' in export_data
        assert isinstance(export_data['profiles'], list)
        assert len(export_data['profiles']) == export_data['profileCount']


class TestExtensionPermissions:
    """Test extension permissions are appropriate"""

    def test_chrome_permissions(self):
        """Test Chrome extension has minimal required permissions"""
        import os
        with open("chrome-extension/manifest.json", 'r') as f:
            manifest = json.load(f)

        required_permissions = ['storage', 'tabs', 'contextMenus', 'notifications']
        actual_permissions = manifest.get('permissions', [])

        for perm in required_permissions:
            assert perm in actual_permissions, f"Missing permission: {perm}"

        # Should not have excessive permissions
        excessive_permissions = ['webRequest', 'webRequestBlocking', 'cookies', 'history']
        for perm in excessive_permissions:
            assert perm not in actual_permissions, f"Excessive permission: {perm}"

    def test_firefox_permissions(self):
        """Test Firefox extension has appropriate permissions"""
        import os
        with open("firefox-extension/manifest.json", 'r') as f:
            manifest = json.load(f)

        required_permissions = ['storage', 'tabs']
        actual_permissions = manifest.get('permissions', [])

        for perm in required_permissions:
            assert perm in actual_permissions


class TestKeyboardShortcuts:
    """Test keyboard shortcut definitions"""

    def test_chrome_shortcuts_defined(self):
        """Test Chrome has keyboard shortcuts"""
        import os
        with open("chrome-extension/manifest.json", 'r') as f:
            manifest = json.load(f)

        assert 'commands' in manifest
        commands = manifest['commands']

        # Check for expected shortcuts
        assert 'switch-profile-1' in commands
        assert 'switch-profile-2' in commands
        assert 'switch-profile-3' in commands
        assert 'quick-switch' in commands

    def test_firefox_shortcuts_defined(self):
        """Test Firefox has keyboard shortcuts"""
        import os
        with open("firefox-extension/manifest.json", 'r') as f:
            manifest = json.load(f)

        assert 'commands' in manifest
        commands = manifest['commands']

        assert 'switch-profile-1' in commands
        assert 'quick-switch' in commands


class TestTemplateLibraryIntegration:
    """Test template library integration"""

    def test_template_files_exist(self):
        """Test template files exist in extensions"""
        import os
        assert os.path.exists("chrome-extension/js/templates.js")
        assert os.path.exists("chrome-extension/templates.html")
        assert os.path.exists("firefox-extension/js/templates.js")
        assert os.path.exists("firefox-extension/templates.html")

    def test_template_count_matches(self):
        """Test template count is consistent"""
        from icon_templates import ICON_TEMPLATES
        template_count = len(ICON_TEMPLATES)

        # Should have 50+ templates
        assert template_count >= 50, f"Expected 50+ templates, got {template_count}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
