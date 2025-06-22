// Browser Profile Icons - Popup Script
// Handles the extension popup interface

document.addEventListener('DOMContentLoaded', async () => {
  const profileList = document.getElementById('profile-list');
  const addProfileBtn = document.getElementById('add-profile');
  const upgradeBtn = document.getElementById('upgrade-btn');
  const profileCount = document.getElementById('profile-count');
  
  // Check Pro status
  const { isPro } = await chrome.runtime.sendMessage({ action: 'checkLicense' });
  
  // Load and display profiles
  const { profiles } = await chrome.runtime.sendMessage({ action: 'getProfiles' });
  
  if (!isPro) {
    profileCount.textContent = `${profiles.length}/5 profiles (Free)`;
    if (profiles.length >= 5) {
      addProfileBtn.disabled = true;
      addProfileBtn.textContent = 'Upgrade for More';
    }
    upgradeBtn.style.display = 'block';
  } else {
    profileCount.textContent = `${profiles.length} profiles (Pro)`;
    upgradeBtn.style.display = 'none';
  }
  
  // Display profiles
  profiles.forEach(profile => {
    const profileEl = createProfileElement(profile, isPro);
    profileList.appendChild(profileEl);
  });
  
  // Add profile button
  addProfileBtn.addEventListener('click', async () => {
    if (!isPro && profiles.length >= 5) {
      chrome.runtime.sendMessage({ action: 'purchasePro' });
      return;
    }
    
    // Open profile creation page
    chrome.tabs.create({ url: 'options.html#new-profile' });
  });
  
  // Upgrade button
  upgradeBtn.addEventListener('click', () => {
    chrome.runtime.sendMessage({ action: 'purchasePro' });
  });
});

function createProfileElement(profile, isPro) {
  const div = document.createElement('div');
  div.className = 'profile-item';
  
  const icon = document.createElement('div');
  icon.className = 'profile-icon';
  icon.style.backgroundColor = profile.color || '#4285f4';
  icon.textContent = profile.name.charAt(0).toUpperCase();
  
  const name = document.createElement('span');
  name.className = 'profile-name';
  name.textContent = profile.name;
  
  const actions = document.createElement('div');
  actions.className = 'profile-actions';
  
  // Switch button
  const switchBtn = document.createElement('button');
  switchBtn.textContent = 'Switch';
  switchBtn.addEventListener('click', async () => {
    const result = await chrome.runtime.sendMessage({ 
      action: 'switchProfile', 
      profileId: profile.id 
    });
    
    if (result.success) {
      window.close();
    } else {
      alert('Failed to switch profile: ' + result.error);
    }
  });
  
  // Edit button (Pro only)
  if (isPro) {
    const editBtn = document.createElement('button');
    editBtn.textContent = 'Edit';
    editBtn.addEventListener('click', () => {
      chrome.tabs.create({ url: `options.html#edit-${profile.id}` });
    });
    actions.appendChild(editBtn);
  }
  
  actions.appendChild(switchBtn);
  
  div.appendChild(icon);
  div.appendChild(name);
  div.appendChild(actions);
  
  return div;
}

// Add Pro features indicator
function showProFeatures() {
  const features = [
    'Unlimited profiles',
    'Cloud sync',
    'Keyboard shortcuts',
    'Custom themes',
    'Extension management',
    'Import/Export'
  ];
  
  const featureList = document.createElement('div');
  featureList.className = 'pro-features';
  featureList.innerHTML = '<h3>Pro Features:</h3>';
  
  features.forEach(feature => {
    const item = document.createElement('div');
    item.textContent = '✓ ' + feature;
    featureList.appendChild(item);
  });
  
  document.body.appendChild(featureList);
}