// Browser Profile Icons - Background Script
// Simplified version without Pro features

// Initialize extension
chrome.runtime.onInstalled.addListener(async (details) => {
  if (details.reason === 'install') {
    // Set default values
    await chrome.storage.local.set({
      profiles: [],
      installedDate: new Date().toISOString()
    });

    // Open welcome page
    chrome.tabs.create({
      url: 'welcome.html'
    });
  }
});

// Handle profile switching
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'switchProfile') {
    handleProfileSwitch(request.profile)
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true;
  }

  if (request.action === 'getProfiles') {
    getProfiles()
      .then(profiles => sendResponse({ profiles }))
      .catch(error => sendResponse({ profiles: [], error: error.message }));
    return true;
  }

  if (request.action === 'saveProfile') {
    saveProfile(request.profile)
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true;
  }

  if (request.action === 'deleteProfile') {
    deleteProfile(request.profileId)
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true;
  }
});

// Switch browser profile
async function handleProfileSwitch(profile) {
  try {
    // Show notification
    await chrome.notifications.create({
      type: 'basic',
      iconUrl: 'images/icon128.png',
      title: 'Profile Switched',
      message: `Switched to ${profile.name}`
    });

    // Apply theme if provided
    if (profile.theme && chrome.theme) {
      await applyTheme(profile.theme);
    }

    return { success: true };
  } catch (error) {
    console.error('Error switching profile:', error);
    return { success: false, error: error.message };
  }
}

// Apply theme to browser
async function applyTheme(theme) {
  if (!chrome.theme) return;

  try {
    if (theme.reset) {
      await chrome.theme.reset();
    } else {
      await chrome.theme.update(theme);
    }
  } catch (error) {
    console.error('Error applying theme:', error);
  }
}

// Get all profiles
async function getProfiles() {
  const data = await chrome.storage.local.get(['profiles']);
  return data.profiles || [];
}

// Save profile
async function saveProfile(profile) {
  try {
    const data = await chrome.storage.local.get(['profiles']);
    const profiles = data.profiles || [];

    const index = profiles.findIndex(p => p.id === profile.id);
    if (index >= 0) {
      profiles[index] = profile;
    } else {
      profiles.push(profile);
    }

    await chrome.storage.local.set({ profiles });
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Delete profile
async function deleteProfile(profileId) {
  try {
    const data = await chrome.storage.local.get(['profiles']);
    const profiles = (data.profiles || []).filter(p => p.id !== profileId);

    await chrome.storage.local.set({ profiles });
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Handle keyboard shortcuts
chrome.commands.onCommand.addListener(async (command) => {
  const data = await chrome.storage.local.get(['profiles']);
  const profiles = data.profiles || [];

  if (command.startsWith('switch-profile-')) {
    const index = parseInt(command.split('-')[2]) - 1;

    if (profiles[index]) {
      await handleProfileSwitch(profiles[index]);
    }
  } else if (command === 'quick-switch') {
    // Open popup
    chrome.action.openPopup();
  }
});

// Context menu
chrome.contextMenus.create({
  id: 'switch-profile',
  title: 'Switch Profile',
  contexts: ['action']
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === 'switch-profile') {
    chrome.action.openPopup();
  }
});
