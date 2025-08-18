// Browser Profile Icons Pro - Popup Script
const FREE_PROFILE_LIMIT = 5;
const PRO_PRICE = 4.99;
const CHROME_STORE_URL = 'https://chrome.google.com/webstore/detail/YOUR_EXTENSION_ID';

class ProfileManager {
  constructor() {
    this.profiles = [];
    this.isPro = false;
    this.init();
  }

  async init() {
    await this.loadProfiles();
    await this.checkProStatus();
    this.render();
    this.attachEventListeners();
  }

  async loadProfiles() {
    const result = await chrome.storage.sync.get(['profiles']);
    this.profiles = result.profiles || this.getDefaultProfiles();
  }

  async checkProStatus() {
    const result = await chrome.storage.sync.get(['isPro', 'licenseKey']);
    this.isPro = result.isPro || false;
    
    // Check with license server
    if (result.licenseKey) {
      this.isPro = await this.validateLicense(result.licenseKey);
    }
  }

  async validateLicense(key) {
    // In production, validate with your server
    // For now, simple check
    return key && key.length === 24;
  }

  getDefaultProfiles() {
    return [
      { id: 1, name: 'Work', icon: '💼', color: '#2196F3' },
      { id: 2, name: 'Personal', icon: '🏠', color: '#4CAF50' },
      { id: 3, name: 'Development', icon: '💻', color: '#FF9800' }
    ];
  }

  render() {
    const container = document.getElementById('profiles');
    container.innerHTML = '';

    this.profiles.forEach((profile, index) => {
      const profileEl = this.createProfileElement(profile, index);
      container.appendChild(profileEl);
    });

    this.updateUI();
  }

  createProfileElement(profile, index) {
    const div = document.createElement('div');
    div.className = 'profile';
    div.innerHTML = `
      <span class="profile-icon" style="background-color: ${profile.color}">${profile.icon}</span>
      <span class="profile-name">${profile.name}</span>
      <div class="profile-actions">
        <button class="edit-btn" data-id="${profile.id}">✏️</button>
        <button class="delete-btn" data-id="${profile.id}">🗑️</button>
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
    const limitReached = !this.isPro && count >= FREE_PROFILE_LIMIT;
    
    document.getElementById('profileCount').textContent = 
      this.isPro ? `${count} profiles` : `${count}/${FREE_PROFILE_LIMIT} profiles`;
    
    document.getElementById('freeLimit').style.display = 
      limitReached ? 'block' : 'none';
    
    document.getElementById('addProfile').disabled = limitReached;
    
    // Update pro features
    document.querySelectorAll('.pro-feature').forEach(el => {
      el.disabled = !this.isPro;
      if (!this.isPro) {
        el.title = 'Pro feature - Upgrade to unlock';
      }
    });
  }

  attachEventListeners() {
    document.getElementById('addProfile').addEventListener('click', () => {
      this.addProfile();
    });

    document.getElementById('upgradePro').addEventListener('click', () => {
      this.upgradeToPro();
    });

    document.getElementById('syncProfiles').addEventListener('click', () => {
      this.syncProfiles();
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
    if (!this.isPro && this.profiles.length >= FREE_PROFILE_LIMIT) {
      this.showUpgradePrompt();
      return;
    }

    const name = prompt('Profile name:');
    if (!name) return;

    const profile = {
      id: Date.now(),
      name: name,
      icon: this.getRandomEmoji(),
      color: this.getRandomColor()
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
    chrome.runtime.sendMessage({
      action: 'switchProfile',
      profile: profile
    });
    
    // Visual feedback
    const feedback = document.createElement('div');
    feedback.className = 'switch-feedback';
    feedback.textContent = `Switched to ${profile.name}`;
    document.body.appendChild(feedback);
    
    setTimeout(() => {
      feedback.remove();
      window.close();
    }, 1000);
  }

  async syncProfiles() {
    if (!this.isPro) {
      this.showUpgradePrompt();
      return;
    }

    // Sync with cloud storage
    try {
      const response = await fetch('https://api.profileicons.com/sync', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${await this.getLicenseKey()}`
        },
        body: JSON.stringify({ profiles: this.profiles })
      });

      if (response.ok) {
        this.showMessage('Profiles synced!');
      }
    } catch (error) {
      console.error('Sync failed:', error);
      this.showMessage('Sync failed. Please try again.');
    }
  }

  async upgradeToPro() {
    // Open Chrome Web Store or payment page
    chrome.tabs.create({
      url: `${CHROME_STORE_URL}?sku=pro_upgrade`
    });
  }

  showUpgradePrompt() {
    const modal = document.createElement('div');
    modal.className = 'upgrade-modal';
    modal.innerHTML = `
      <div class="modal-content">
        <h2>Upgrade to Pro</h2>
        <ul>
          <li>✅ Unlimited profiles</li>
          <li>✅ Cloud sync across devices</li>
          <li>✅ Custom themes & icons</li>
          <li>✅ Keyboard shortcuts</li>
          <li>✅ Priority support</li>
        </ul>
        <button class="upgrade-btn" onclick="profileManager.upgradeToPro()">
          Upgrade for $${PRO_PRICE}
        </button>
        <button class="cancel-btn" onclick="this.parentElement.parentElement.remove()">
          Maybe later
        </button>
      </div>
    `;
    document.body.appendChild(modal);
  }

  async saveProfiles() {
    await chrome.storage.sync.set({ profiles: this.profiles });
  }

  async getLicenseKey() {
    const result = await chrome.storage.sync.get(['licenseKey']);
    return result.licenseKey;
  }

  getRandomEmoji() {
    const emojis = ['🎯', '🚀', '💡', '🎨', '📊', '🔧', '📚', '🎮', '🎵', '🏃'];
    return emojis[Math.floor(Math.random() * emojis.length)];
  }

  getRandomColor() {
    const colors = ['#F44336', '#E91E63', '#9C27B0', '#673AB7', '#3F51B5', 
                    '#2196F3', '#03A9F4', '#00BCD4', '#009688', '#4CAF50'];
    return colors[Math.floor(Math.random() * colors.length)];
  }

  showMessage(text) {
    const msg = document.createElement('div');
    msg.className = 'message';
    msg.textContent = text;
    document.body.appendChild(msg);
    setTimeout(() => msg.remove(), 3000);
  }
}

// Initialize
const profileManager = new ProfileManager();