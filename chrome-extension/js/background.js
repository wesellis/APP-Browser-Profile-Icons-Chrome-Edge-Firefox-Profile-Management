// Browser Profile Icons - Background Script
// Handles profile management and Pro features

// Constants
const FREE_PROFILE_LIMIT = 5;
const PRO_SKU = 'browser_profile_icons_pro';
const TRIAL_DAYS = 7;

// Initialize extension
chrome.runtime.onInstalled.addListener(async (details) => {
  if (details.reason === 'install') {
    // Set default values
    await chrome.storage.sync.set({
      isPro: false,
      profiles: [],
      installedDate: new Date().toISOString(),
      trialUsed: false
    });
    
    // Open welcome page
    chrome.tabs.create({
      url: 'chrome-extension://' + chrome.runtime.id + '/welcome.html'
    });
  }
  
  // Check license status
  await checkLicenseStatus();
});

// Check if user has Pro version
async function checkLicenseStatus() {
  try {
    // Check for in-app purchase
    if (chrome.payments && chrome.payments.status) {
      const status = await chrome.payments.status.get({
        sku: PRO_SKU
      });
      
      if (status && status.state === 'ACTIVE') {
        await chrome.storage.sync.set({ isPro: true });
        return true;
      }
    }
    
    // Check trial status
    const data = await chrome.storage.sync.get(['installedDate', 'trialUsed']);
    if (!data.trialUsed && data.installedDate) {
      const installDate = new Date(data.installedDate);
      const daysSinceInstall = (new Date() - installDate) / (1000 * 60 * 60 * 24);
      
      if (daysSinceInstall <= TRIAL_DAYS) {
        // Still in trial period
        return true;
      } else {
        // Trial expired
        await chrome.storage.sync.set({ trialUsed: true });
      }
    }
    
    return false;
  } catch (error) {
    console.error('Error checking license:', error);
    return false;
  }
}

// Handle profile switching
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'switchProfile') {
    handleProfileSwitch(request.profileId)
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Keep message channel open for async response
  }
  
  if (request.action === 'checkLicense') {
    checkLicenseStatus()
      .then(isPro => sendResponse({ isPro }))
      .catch(() => sendResponse({ isPro: false }));
    return true;
  }
  
  if (request.action === 'purchasePro') {
    initiatePurchase()
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
});

// Switch browser profile
async function handleProfileSwitch(profileId) {
  try {
    const data = await chrome.storage.sync.get(['profiles', 'isPro']);
    const profile = data.profiles.find(p => p.id === profileId);
    
    if (!profile) {
      throw new Error('Profile not found');
    }
    
    // Apply profile settings
    if (profile.theme) {
      await applyTheme(profile.theme);
    }
    
    if (profile.bookmarks && data.isPro) {
      await syncBookmarks(profile.bookmarks);
    }
    
    if (profile.extensions && data.isPro) {
      await toggleExtensions(profile.extensions);
    }
    
    // Update last used
    profile.lastUsed = new Date().toISOString();
    await chrome.storage.sync.set({ profiles: data.profiles });
    
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

// Sync bookmarks (Pro feature)
async function syncBookmarks(bookmarkData) {
  // This is a Pro feature - implement bookmark syncing
  console.log('Syncing bookmarks (Pro feature)');
}

// Toggle extensions (Pro feature)
async function toggleExtensions(extensionList) {
  if (!chrome.management) return;
  
  try {
    for (const ext of extensionList) {
      if (ext.id !== chrome.runtime.id) { // Don't disable ourselves!
        await chrome.management.setEnabled(ext.id, ext.enabled);
      }
    }
  } catch (error) {
    console.error('Error toggling extensions:', error);
  }
}

// Get all profiles
async function getProfiles() {
  const data = await chrome.storage.sync.get(['profiles', 'isPro']);
  const profiles = data.profiles || [];
  const isPro = data.isPro || false;
  
  // Limit profiles for free version
  if (!isPro && profiles.length > FREE_PROFILE_LIMIT) {
    return profiles.slice(0, FREE_PROFILE_LIMIT);
  }
  
  return profiles;
}

// Initiate Pro purchase
async function initiatePurchase() {
  try {
    if (!chrome.payments || !chrome.payments.buy) {
      // Fallback to external purchase link
      chrome.tabs.create({
        url: 'https://gumroad.com/l/browser-profile-icons-pro'
      });
      return { success: true, external: true };
    }
    
    // Chrome Web Store in-app purchase
    const response = await chrome.payments.buy({
      sku: PRO_SKU,
      // Chrome handles payment UI
    });
    
    if (response && response.response === 'ok') {
      await chrome.storage.sync.set({ isPro: true });
      return { success: true };
    }
    
    return { success: false, error: 'Purchase cancelled' };
  } catch (error) {
    console.error('Purchase error:', error);
    return { success: false, error: error.message };
  }
}

// Handle keyboard shortcuts
chrome.commands.onCommand.addListener(async (command) => {
  const data = await chrome.storage.sync.get(['profiles', 'isPro']);
  
  if (!data.isPro && command !== 'quick-switch-1') {
    // Only allow first shortcut in free version
    showUpgradeNotification();
    return;
  }
  
  if (command.startsWith('quick-switch-')) {
    const index = parseInt(command.split('-')[2]) - 1;
    const profiles = data.profiles || [];
    
    if (profiles[index]) {
      await handleProfileSwitch(profiles[index].id);
    }
  }
});

// Show upgrade notification
function showUpgradeNotification() {
  chrome.notifications.create({
    type: 'basic',
    iconUrl: '/images/icon-128.png',
    title: 'Pro Feature',
    message: 'Keyboard shortcuts are a Pro feature. Upgrade to unlock!',
    buttons: [{ title: 'Upgrade Now' }]
  });
}

// Handle notification clicks
chrome.notifications.onButtonClicked.addListener((notificationId, buttonIndex) => {
  if (buttonIndex === 0) {
    initiatePurchase();
  }
});

// Track usage for analytics
async function trackEvent(category, action, label = null) {
  // Simple analytics tracking
  const data = await chrome.storage.local.get(['analytics']);
  const analytics = data.analytics || { events: [] };
  
  analytics.events.push({
    category,
    action,
    label,
    timestamp: new Date().toISOString()
  });
  
  // Keep only last 1000 events
  if (analytics.events.length > 1000) {
    analytics.events = analytics.events.slice(-1000);
  }
  
  await chrome.storage.local.set({ analytics });
}

// Export analytics (Pro feature)
async function exportAnalytics() {
  const data = await chrome.storage.local.get(['analytics']);
  const analytics = data.analytics || { events: [] };
  
  const csv = 'Category,Action,Label,Timestamp\n' + 
    analytics.events.map(e => 
      `"${e.category}","${e.action}","${e.label || ''}","${e.timestamp}"`
    ).join('\n');
  
  return csv;
}

// Listen for uninstall to clean up
chrome.runtime.setUninstallURL('https://forms.gle/feedback-form-url');