// Browser Profile Icons - Options/Settings Page

class SettingsManager {
  constructor() {
    this.init();
  }

  init() {
    this.attachEventListeners();
  }

  attachEventListeners() {
    document.getElementById('exportBtn').addEventListener('click', () => {
      this.exportProfiles();
    });

    document.getElementById('importBtn').addEventListener('click', () => {
      document.getElementById('fileInput').click();
    });

    document.getElementById('fileInput').addEventListener('change', (e) => {
      this.importProfiles(e);
    });

    document.getElementById('resetBtn').addEventListener('click', () => {
      this.resetToDefaults();
    });

    document.getElementById('clearBtn').addEventListener('click', () => {
      this.clearAllData();
    });
  }

  async exportProfiles() {
    try {
      const data = await browser.storage.local.get(['profiles']);
      const profiles = data.profiles || [];

      const exportData = {
        version: '3.0.0',
        exportDate: new Date().toISOString(),
        profileCount: profiles.length,
        profiles: profiles
      };

      const blob = new Blob([JSON.stringify(exportData, null, 2)], {
        type: 'application/json'
      });

      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `browser-profiles-${new Date().toISOString().split('T')[0]}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      this.showSuccess('Profiles exported successfully!');
    } catch (error) {
      console.error('Error exporting profiles:', error);
      alert('Error exporting profiles. Please try again.');
    }
  }

  async importProfiles(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async (e) => {
      try {
        const data = JSON.parse(e.target.result);

        if (!data.profiles || !Array.isArray(data.profiles)) {
          throw new Error('Invalid file format');
        }

        await browser.storage.local.set({ profiles: data.profiles });
        this.showSuccess(`Imported ${data.profiles.length} profiles successfully!`);

        // Reset file input
        event.target.value = '';
      } catch (error) {
        console.error('Error importing profiles:', error);
        alert('Error importing profiles. Please check the file format.');
      }
    };

    reader.readAsText(file);
  }

  async resetToDefaults() {
    if (!confirm('Reset to default profiles? This will replace your current profiles.')) {
      return;
    }

    const defaultProfiles = [
      { id: 1, name: 'Work', icon: '💼', color: '#2196F3', created: new Date().toISOString() },
      { id: 2, name: 'Personal', icon: '🏠', color: '#4CAF50', created: new Date().toISOString() },
      { id: 3, name: 'Development', icon: '💻', color: '#FF9800', created: new Date().toISOString() }
    ];

    try {
      await browser.storage.local.set({ profiles: defaultProfiles });
      this.showSuccess('Profiles reset to defaults!');
    } catch (error) {
      console.error('Error resetting profiles:', error);
      alert('Error resetting profiles. Please try again.');
    }
  }

  async clearAllData() {
    if (!confirm('Delete ALL profiles and settings? This cannot be undone!')) {
      return;
    }

    if (!confirm('Are you absolutely sure? All your profiles will be permanently deleted.')) {
      return;
    }

    try {
      await browser.storage.local.clear();
      this.showSuccess('All data cleared successfully!');

      // Reload after a moment
      setTimeout(() => {
        location.reload();
      }, 1500);
    } catch (error) {
      console.error('Error clearing data:', error);
      alert('Error clearing data. Please try again.');
    }
  }

  showSuccess(message) {
    const successEl = document.getElementById('successMessage');
    successEl.textContent = message;
    successEl.style.display = 'block';

    setTimeout(() => {
      successEl.style.display = 'none';
    }, 3000);
  }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  new SettingsManager();
});
