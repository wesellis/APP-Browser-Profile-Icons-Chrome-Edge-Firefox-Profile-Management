// Browser Profile Icons - Firefox Background Script
// Simplified version for Firefox

// Initialize extension
browser.runtime.onInstalled.addListener(async (details) => {
  if (details.reason === 'install') {
    // Set default values
    await browser.storage.local.set({
      profiles: [],
      installedDate: new Date().toISOString()
    });

    // Open welcome page
    browser.tabs.create({
      url: browser.runtime.getURL('welcome.html')
    });
  }
});

// Handle profile switching
browser.runtime.onMessage.addListener(async (request, sender, sendResponse) => {
  if (request.action === 'switchProfile') {
    return handleProfileSwitch(request.profile);
  }

  if (request.action === 'getProfiles') {
    return getProfiles();
  }

  if (request.action === 'saveProfile') {
    return saveProfile(request.profile);
  }

  if (request.action === 'deleteProfile') {
    return deleteProfile(request.profileId);
  }
});

// Switch browser profile
async function handleProfileSwitch(profile) {
  try {
    // Show notification
    await browser.notifications.create({
      type: 'basic',
      iconUrl: browser.runtime.getURL('images/icon128.png'),
      title: 'Profile Switched',
      message: `Switched to ${profile.name}`
    });

    // Apply theme if supported
    if (profile.theme && browser.theme) {
      await applyTheme(profile.theme);
    }

    return { success: true };
  } catch (error) {
    console.error('Error switching profile:', error);
    return { success: false, error: error.message };
  }
}

// Apply theme
async function applyTheme(theme) {
  if (!browser.theme) return;

  try {
    if (theme.reset) {
      await browser.theme.reset();
    } else {
      await browser.theme.update(theme);
    }
  } catch (error) {
    console.error('Error applying theme:', error);
  }
}

// Get all profiles
async function getProfiles() {
  try {
    const data = await browser.storage.local.get(['profiles']);
    return { profiles: data.profiles || [] };
  } catch (error) {
    return { profiles: [], error: error.message };
  }
}

// Save profile
async function saveProfile(profile) {
  try {
    const data = await browser.storage.local.get(['profiles']);
    const profiles = data.profiles || [];

    const index = profiles.findIndex(p => p.id === profile.id);
    if (index >= 0) {
      profiles[index] = profile;
    } else {
      profiles.push(profile);
    }

    await browser.storage.local.set({ profiles });
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Delete profile
async function deleteProfile(profileId) {
  try {
    const data = await browser.storage.local.get(['profiles']);
    const profiles = (data.profiles || []).filter(p => p.id !== profileId);

    await browser.storage.local.set({ profiles });
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Handle keyboard shortcuts
browser.commands.onCommand.addListener(async (command) => {
  const data = await browser.storage.local.get(['profiles']);
  const profiles = data.profiles || [];

  if (command.startsWith('switch-profile-')) {
    const index = parseInt(command.split('-')[2]) - 1;

    if (profiles[index]) {
      await handleProfileSwitch(profiles[index]);
    }
  } else if (command === 'quick-switch') {
    // Show quick switch UI
    browser.browserAction.openPopup();
  }
});

// Context menu
browser.contextMenus.create({
  id: 'switch-profile',
  title: 'Switch Profile',
  contexts: ['browser_action']
});

browser.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === 'switch-profile') {
    browser.browserAction.openPopup();
  }
});
