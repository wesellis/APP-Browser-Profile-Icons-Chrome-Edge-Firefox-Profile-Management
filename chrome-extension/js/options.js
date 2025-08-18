// Browser Profile Icons - Options Page
document.addEventListener('DOMContentLoaded', async () => {
  // Check license status
  const { isPro } = await chrome.runtime.sendMessage({ action: 'checkLicense' });
  updateUIForLicense(isPro);
  
  // Load current settings
  loadSettings();
  
  // Tab switching
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
      const tabName = tab.dataset.tab;
      switchTab(tabName);
    });
  });
  
  // Add profile button
  document.getElementById('add-profile-btn').addEventListener('click', () => {
    showProfileModal();
  });
  
  // Profile form submission
  document.getElementById('profile-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    await saveProfile();
  });
  
  // Cancel modal
  document.getElementById('cancel-modal').addEventListener('click', () => {
    hideProfileModal();
  });
  
  // Settings change handlers
  document.getElementById('show-notifications').addEventListener('change', saveSettings);
  document.getElementById('enable-shortcuts').addEventListener('change', saveSettings);
  document.getElementById('auto-switch').addEventListener('change', saveSettings);
  document.getElementById('sync-enabled').addEventListener('change', saveSettings);
  document.getElementById('theme-select').addEventListener('change', saveSettings);
  document.getElementById('icon-style').addEventListener('change', saveSettings);
  
  // Upgrade buttons
  document.querySelectorAll('[id^="upgrade-"]').forEach(btn => {
    btn.addEventListener('click', () => {
      chrome.runtime.sendMessage({ action: 'purchasePro' });
    });
  });
  
  // Export/Import
  if (isPro) {
    document.getElementById('export-profiles').addEventListener('click', exportProfiles);
    document.getElementById('import-file').addEventListener('change', importProfiles);
    document.getElementById('sync-now').addEventListener('click', syncProfiles);
  }
  
  // Load profiles
  loadProfiles();
});

function updateUIForLicense(isPro) {
  const licenseStatus = document.getElementById('license-status');
  const licenseType = document.getElementById('license-type');
  
  if (isPro) {
    licenseStatus.innerHTML = '<span class="pro-badge">PRO</span>';
    licenseType.textContent = 'Pro';
    
    // Enable Pro features
    document.getElementById('profile-icon').disabled = false;
    document.getElementById('enable-shortcuts').disabled = false;
    document.getElementById('auto-switch').disabled = false;
    document.getElementById('sync-enabled').disabled = false;
    
    // Show backup section
    document.getElementById('pro-notice').style.display = 'none';
    document.getElementById('backup-section').style.display = 'block';
  } else {
    licenseStatus.innerHTML = '<span class="free-badge">FREE</span>';
    licenseType.textContent = 'Free (5 profiles limit)';
  }
}

async function loadSettings() {
  const settings = await chrome.storage.sync.get([
    'showNotifications',
    'enableShortcuts',
    'autoSwitch',
    'syncEnabled',
    'theme',
    'iconStyle'
  ]);
  
  document.getElementById('show-notifications').checked = settings.showNotifications ?? true;
  document.getElementById('enable-shortcuts').checked = settings.enableShortcuts ?? false;
  document.getElementById('auto-switch').checked = settings.autoSwitch ?? false;
  document.getElementById('sync-enabled').checked = settings.syncEnabled ?? false;
  document.getElementById('theme-select').value = settings.theme ?? 'system';
  document.getElementById('icon-style').value = settings.iconStyle ?? 'initials';
}

async function saveSettings() {
  const settings = {
    showNotifications: document.getElementById('show-notifications').checked,
    enableShortcuts: document.getElementById('enable-shortcuts').checked,
    autoSwitch: document.getElementById('auto-switch').checked,
    syncEnabled: document.getElementById('sync-enabled').checked,
    theme: document.getElementById('theme-select').value,
    iconStyle: document.getElementById('icon-style').value
  };
  
  await chrome.storage.sync.set(settings);
  showMessage('Settings saved!');
}

async function loadProfiles() {
  const { profiles } = await chrome.runtime.sendMessage({ action: 'getProfiles' });
  const grid = document.getElementById('profile-grid');
  
  grid.innerHTML = '';
  
  profiles.forEach(profile => {
    const card = createProfileCard(profile);
    grid.appendChild(card);
  });
}

function createProfileCard(profile) {
  const card = document.createElement('div');
  card.className = 'profile-card';
  
  card.innerHTML = `
    <div class="profile-icon-large" style="background-color: ${profile.color}">
      ${profile.name.charAt(0).toUpperCase()}
    </div>
    <h3>${profile.name}</h3>
    <div class="profile-actions">
      <button class="btn btn-small" onclick="editProfile('${profile.id}')">Edit</button>
      <button class="btn btn-small btn-danger" onclick="deleteProfile('${profile.id}')">Delete</button>
    </div>
  `;
  
  return card;
}

function showProfileModal(profile = null) {
  const modal = document.getElementById('profile-modal');
  const title = document.getElementById('modal-title');
  
  if (profile) {
    title.textContent = 'Edit Profile';
    document.getElementById('profile-name').value = profile.name;
    document.getElementById('profile-color').value = profile.color;
    document.getElementById('profile-default').checked = profile.isDefault;
  } else {
    title.textContent = 'New Profile';
    document.getElementById('profile-form').reset();
  }
  
  modal.style.display = 'flex';
}

function hideProfileModal() {
  document.getElementById('profile-modal').style.display = 'none';
}

async function saveProfile() {
  const name = document.getElementById('profile-name').value;
  const color = document.getElementById('profile-color').value;
  const isDefault = document.getElementById('profile-default').checked;
  
  const profile = {
    id: Date.now().toString(),
    name,
    color,
    isDefault,
    createdAt: new Date().toISOString()
  };
  
  const { profiles } = await chrome.storage.sync.get(['profiles']);
  const allProfiles = profiles || [];
  
  // Check profile limit for free users
  const { isPro } = await chrome.runtime.sendMessage({ action: 'checkLicense' });
  if (!isPro && allProfiles.length >= 5) {
    alert('Free version is limited to 5 profiles. Upgrade to Pro for unlimited profiles!');
    chrome.runtime.sendMessage({ action: 'purchasePro' });
    return;
  }
  
  allProfiles.push(profile);
  await chrome.storage.sync.set({ profiles: allProfiles });
  
  hideProfileModal();
  loadProfiles();
  showMessage('Profile created successfully!');
}

window.editProfile = async function(profileId) {
  const { profiles } = await chrome.storage.sync.get(['profiles']);
  const profile = profiles.find(p => p.id === profileId);
  if (profile) {
    showProfileModal(profile);
  }
};

window.deleteProfile = async function(profileId) {
  if (!confirm('Are you sure you want to delete this profile?')) {
    return;
  }
  
  const { profiles } = await chrome.storage.sync.get(['profiles']);
  const filtered = profiles.filter(p => p.id !== profileId);
  await chrome.storage.sync.set({ profiles: filtered });
  
  loadProfiles();
  showMessage('Profile deleted');
};

function switchTab(tabName) {
  // Update tab buttons
  document.querySelectorAll('.tab').forEach(tab => {
    tab.classList.toggle('active', tab.dataset.tab === tabName);
  });
  
  // Update tab content
  document.querySelectorAll('.tab-content').forEach(content => {
    content.classList.toggle('active', content.id === `${tabName}-tab`);
  });
}

async function exportProfiles() {
  const data = await chrome.storage.sync.get(['profiles', 'settings']);
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  
  const a = document.createElement('a');
  a.href = url;
  a.download = `browser-profiles-backup-${new Date().toISOString().split('T')[0]}.json`;
  a.click();
  
  URL.revokeObjectURL(url);
  showMessage('Profiles exported successfully!');
}

async function importProfiles(event) {
  const file = event.target.files[0];
  if (!file) return;
  
  try {
    const text = await file.text();
    const data = JSON.parse(text);
    
    if (data.profiles) {
      await chrome.storage.sync.set({ profiles: data.profiles });
      if (data.settings) {
        await chrome.storage.sync.set(data.settings);
      }
      
      loadProfiles();
      loadSettings();
      showMessage('Profiles imported successfully!');
    }
  } catch (error) {
    alert('Failed to import profiles. Please check the file format.');
  }
}

async function syncProfiles() {
  const statusText = document.querySelector('.sync-status .status-text');
  statusText.textContent = 'Syncing...';
  
  // Simulate sync (in real app, this would sync with cloud service)
  setTimeout(() => {
    statusText.textContent = 'Synced just now';
    showMessage('Profiles synced successfully!');
  }, 2000);
}

function showMessage(text) {
  const message = document.createElement('div');
  message.className = 'message';
  message.textContent = text;
  document.body.appendChild(message);
  
  setTimeout(() => {
    message.remove();
  }, 3000);
}