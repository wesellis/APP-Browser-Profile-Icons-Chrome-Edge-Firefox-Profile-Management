// Browser Profile Icons - Chrome Popup Script
// Simplified version without Pro features

class ProfileManager {
  constructor() {
    this.profiles = [];
    this.init();
  }

  async init() {
    await this.loadProfiles();
    this.render();
    this.attachEventListeners();
  }

  async loadProfiles() {
    try {
      const result = await chrome.storage.local.get(['profiles']);
      this.profiles = result.profiles || this.getDefaultProfiles();
    } catch (error) {
      console.error('Error loading profiles:', error);
      this.profiles = this.getDefaultProfiles();
    }
  }

  getDefaultProfiles() {
    return [
      { id: 1, name: 'Work', icon: '💼', color: '#2196F3', created: new Date().toISOString() },
      { id: 2, name: 'Personal', icon: '🏠', color: '#4CAF50', created: new Date().toISOString() },
      { id: 3, name: 'Development', icon: '💻', color: '#FF9800', created: new Date().toISOString() }
    ];
  }

  render() {
    const container = document.getElementById('profiles');
    container.innerHTML = '';

    if (this.profiles.length === 0) {
      container.innerHTML = `
        <div class="empty-state">
          <div class="empty-state-icon">📂</div>
          <p>No profiles yet</p>
          <p style="font-size: 12px; margin-top: 5px;">Click "+ Add Profile" to get started</p>
        </div>
      `;
    } else {
      this.profiles.forEach((profile, index) => {
        const profileEl = this.createProfileElement(profile, index);
        container.appendChild(profileEl);
      });
    }

    this.updateUI();
  }

  createProfileElement(profile, index) {
    const div = document.createElement('div');
    div.className = 'profile';
    div.innerHTML = `
      <span class="profile-icon" style="background-color: ${profile.color}">${profile.icon}</span>
      <span class="profile-name">${profile.name}</span>
      <div class="profile-actions">
        <button class="edit-btn" data-id="${profile.id}" title="Edit">✏️</button>
        <button class="delete-btn" data-id="${profile.id}" title="Delete">🗑️</button>
      </div>
    `;

    div.addEventListener('click', (e) => {
      if (!e.target.closest('.profile-actions')) {
        this.switchProfile(profile);
      }
    });

    return div;
  }

  updateUI() {
    const count = this.profiles.length;
    document.getElementById('profileCount').textContent =
      count === 1 ? '1 profile' : `${count} profiles`;
  }

  attachEventListeners() {
    document.getElementById('addProfile').addEventListener('click', () => {
      this.addProfile();
    });

    document.getElementById('importProfiles').addEventListener('click', () => {
      this.importProfiles();
    });

    document.getElementById('settings').addEventListener('click', () => {
      chrome.runtime.openOptionsPage();
    });

    // Profile action listeners
    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('edit-btn')) {
        const id = parseInt(e.target.dataset.id);
        this.editProfile(id);
      } else if (e.target.classList.contains('delete-btn')) {
        const id = parseInt(e.target.dataset.id);
        this.deleteProfile(id);
      }
    });
  }

  async addProfile() {
    const name = prompt('Profile name:');
    if (!name) return;

    const profile = {
      id: Date.now(),
      name: name,
      icon: this.getRandomEmoji(),
      color: this.getRandomColor(),
      created: new Date().toISOString()
    };

    this.profiles.push(profile);
    await this.saveProfiles();
    this.render();
  }

  async editProfile(id) {
    const profile = this.profiles.find(p => p.id === id);
    if (!profile) return;

    const newName = prompt('Edit profile name:', profile.name);
    if (newName && newName !== profile.name) {
      profile.name = newName;
      await this.saveProfiles();
      this.render();
    }
  }

  async deleteProfile(id) {
    if (confirm('Delete this profile?')) {
      this.profiles = this.profiles.filter(p => p.id !== id);
      await this.saveProfiles();
      this.render();
    }
  }

  async switchProfile(profile) {
    // Send message to background script
    try {
      await chrome.runtime.sendMessage({
        action: 'switchProfile',
        profile: profile
      });

      // Visual feedback
      const feedback = document.createElement('div');
      feedback.className = 'switch-feedback';
      feedback.textContent = `Switched to ${profile.name}`;
      document.body.appendChild(feedback);

      // Update last used
      profile.lastUsed = new Date().toISOString();
      await this.saveProfiles();

      setTimeout(() => {
        feedback.remove();
        window.close();
      }, 1000);
    } catch (error) {
      console.error('Error switching profile:', error);
    }
  }

  async importProfiles() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';

    input.onchange = async (e) => {
      const file = e.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = async (event) => {
        try {
          const data = JSON.parse(event.target.result);
          if (data.profiles && Array.isArray(data.profiles)) {
            this.profiles = data.profiles;
            await this.saveProfiles();
            this.render();
            this.showMessage('Profiles imported successfully!');
          }
        } catch (error) {
          console.error('Error importing profiles:', error);
          alert('Error importing profiles. Please check the file format.');
        }
      };
      reader.readAsText(file);
    };

    input.click();
  }

  async saveProfiles() {
    try {
      await chrome.storage.local.set({ profiles: this.profiles });
    } catch (error) {
      console.error('Error saving profiles:', error);
    }
  }

  getRandomEmoji() {
    const emojis = ['🎯', '🚀', '💡', '🎨', '📊', '🔧', '📚', '🎮', '🎵', '🏃', '🌟', '🔥', '⚡', '🎪', '🎭'];
    return emojis[Math.floor(Math.random() * emojis.length)];
  }

  getRandomColor() {
    const colors = ['#F44336', '#E91E63', '#9C27B0', '#673AB7', '#3F51B5',
                    '#2196F3', '#03A9F4', '#00BCD4', '#009688', '#4CAF50',
                    '#8BC34A', '#CDDC39', '#FFC107', '#FF9800', '#FF5722'];
    return colors[Math.floor(Math.random() * colors.length)];
  }

  showMessage(text) {
    const msg = document.createElement('div');
    msg.className = 'switch-feedback';
    msg.textContent = text;
    document.body.appendChild(msg);
    setTimeout(() => msg.remove(), 2000);
  }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  new ProfileManager();
});
