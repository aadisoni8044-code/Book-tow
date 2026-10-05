// Main Renderer Application Controller
document.addEventListener('DOMContentLoaded', async () => {
  // Elements
  const webView = document.getElementById('web-view');
  const btnBack = document.getElementById('btn-back');
  const btnForward = document.getElementById('btn-forward');
  const btnReload = document.getElementById('btn-reload');
  const btnHome = document.getElementById('btn-home');
  const addressInput = document.getElementById('address-input');
  const searchIndicator = document.getElementById('search-indicator');
  const securityBadge = document.getElementById('security-badge');
  const securityIcon = document.getElementById('security-icon');
  const btnShield = document.getElementById('btn-shield');
  const privacyPanel = document.getElementById('privacy-panel');
  const btnMenu = document.getElementById('btn-menu');
  const menuPanel = document.getElementById('menu-panel');
  const menuNewTab = document.getElementById('menu-new-tab');
  const menuClearNow = document.getElementById('menu-clear-now');
  const menuSettings = document.getElementById('menu-settings');
  const settingsModal = document.getElementById('settings-modal');
  const btnCloseSettings = document.getElementById('btn-close-settings');
  const settingTheme = document.getElementById('setting-theme');
  const settingSearchEngine = document.getElementById('setting-search-engine');

  let currentSettings = {
    theme: 'system',
    homePage: 'app://home',
    searchEngine: 'https://duckduckgo.com/?q='
  };

  // Helper url parser
  function parseAddressInput(input, searchEngine = currentSettings.searchEngine) {
    if (!input) return 'home.html';
    const trimmed = input.trim();
    if (trimmed === 'home.html' || trimmed === 'app://home') return 'home.html';

    const urlWithProtocol = /^(https?:\/\/|file:\/\/|ftp:\/\/)/i;
    const domainPattern = /^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(:\d+)?(\/.*)?$/;
    const localhostPattern = /^localhost(:\d+)?(\/.*)?$/i;
    const ipAddressPattern = /^(\d{1,3}\.){3}\d{1,3}(:\d+)?(\/.*)?$/;

    if (urlWithProtocol.test(trimmed)) return trimmed;
    if (domainPattern.test(trimmed) || localhostPattern.test(trimmed) || ipAddressPattern.test(trimmed)) {
      return `https://${trimmed}`;
    }
    return `${searchEngine}${encodeURIComponent(trimmed)}`;
  }

  function isDirectUrl(input) {
    if (!input) return false;
    const trimmed = input.trim();
    if (trimmed === 'home.html' || trimmed === 'app://home') return true;
    const urlWithProtocol = /^(https?:\/\/|file:\/\/|ftp:\/\/)/i;
    const domainPattern = /^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(:\d+)?(\/.*)?$/;
    const localhostPattern = /^localhost(:\d+)?(\/.*)?$/i;
    const ipAddressPattern = /^(\d{1,3}\.){3}\d{1,3}(:\d+)?(\/.*)?$/;

    return urlWithProtocol.test(trimmed) || domainPattern.test(trimmed) || localhostPattern.test(trimmed) || ipAddressPattern.test(trimmed);
  }

  // Load Settings from Main Process
  if (window.privateBrowser) {
    currentSettings = await window.privateBrowser.getSettings();
    applyTheme(currentSettings.theme);
    if (settingTheme) settingTheme.value = currentSettings.theme;
    if (settingSearchEngine) settingSearchEngine.value = currentSettings.searchEngine;
  }

  function applyTheme(theme) {
    if (theme === 'dark' || theme === 'light') {
      document.documentElement.setAttribute('data-theme', theme);
    } else {
      document.documentElement.removeAttribute('data-theme');
    }
    // Propagate theme to home page webview if needed
    if (webView && webView.contentWindow) {
      try {
        webView.contentWindow.postMessage({ theme }, '*');
      } catch (e) {}
    }
  }

  // Navigation Button Handlers
  btnBack.addEventListener('click', () => {
    if (webView.canGoBack()) webView.goBack();
  });

  btnForward.addEventListener('click', () => {
    if (webView.canGoForward()) webView.goForward();
  });

  btnReload.addEventListener('click', () => {
    if (webView.isLoading()) {
      webView.stop();
    } else {
      webView.reload();
    }
  });

  btnHome.addEventListener('click', () => {
    webView.src = 'home.html';
  });

  // Address Bar Input Listeners
  addressInput.addEventListener('input', () => {
    const value = addressInput.value.trim();
    if (value && !isDirectUrl(value)) {
      searchIndicator.classList.add('active');
    } else {
      searchIndicator.classList.remove('active');
    }
  });

  addressInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const targetUrl = parseAddressInput(addressInput.value, currentSettings.searchEngine);
      webView.src = targetUrl;
      addressInput.blur();
    }
  });

  addressInput.addEventListener('focus', () => {
    addressInput.select();
  });

  // Webview Navigation Events
  webView.addEventListener('did-start-loading', () => {
    btnReload.innerHTML = `<svg viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>`;
    btnReload.title = 'Stop Loading';
  });

  webView.addEventListener('did-stop-loading', () => {
    btnReload.innerHTML = `<svg viewBox="0 0 24 24"><path d="M17.65 6.35A7.958 7.958 0 0012 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08A5.99 5.99 0 0112 18c-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg>`;
    btnReload.title = 'Reload';

    btnBack.disabled = !webView.canGoBack();
    btnForward.disabled = !webView.canGoForward();
  });

  webView.addEventListener('did-navigate', (e) => {
    updateUrlDisplay(e.url);
  });

  webView.addEventListener('did-navigate-in-page', (e) => {
    updateUrlDisplay(e.url);
  });

  function updateUrlDisplay(url) {
    if (!url) return;
    if (url.includes('home.html')) {
      addressInput.value = '';
      securityBadge.classList.add('secure');
      return;
    }

    addressInput.value = url;
    if (url.startsWith('https://')) {
      securityBadge.classList.add('secure');
    } else {
      securityBadge.classList.remove('secure');
    }
  }

  // Listen for message from Home Page
  window.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'START_BROWSING') {
      webView.src = currentSettings.searchEngine.replace('?q=', '');
    }
  });

  // Toggle Privacy Panel
  btnShield.addEventListener('click', (e) => {
    e.stopPropagation();
    menuPanel.classList.remove('show');
    privacyPanel.classList.toggle('show');
  });

  // Toggle Menu Panel
  btnMenu.addEventListener('click', (e) => {
    e.stopPropagation();
    privacyPanel.classList.remove('show');
    menuPanel.classList.toggle('show');
  });

  document.addEventListener('click', () => {
    privacyPanel.classList.remove('show');
    menuPanel.classList.remove('show');
  });

  privacyPanel.addEventListener('click', (e) => e.stopPropagation());
  menuPanel.addEventListener('click', (e) => e.stopPropagation());

  // Menu Options Handlers
  menuNewTab.addEventListener('click', () => {
    menuPanel.classList.remove('show');
    webView.src = 'home.html';
  });

  menuClearNow.addEventListener('click', async () => {
    menuPanel.classList.remove('show');
    if (window.privateBrowser) {
      await window.privateBrowser.clearSessionNow();
    }
    webView.src = 'home.html';
  });

  menuSettings.addEventListener('click', () => {
    menuPanel.classList.remove('show');
    settingsModal.classList.add('active');
  });

  btnCloseSettings.addEventListener('click', () => {
    settingsModal.classList.remove('active');
  });

  // Save Settings Handlers
  settingTheme.addEventListener('change', async () => {
    const newTheme = settingTheme.value;
    currentSettings.theme = newTheme;
    applyTheme(newTheme);
    if (window.privateBrowser) {
      await window.privateBrowser.saveSettings({ theme: newTheme });
    }
  });

  settingSearchEngine.addEventListener('change', async () => {
    const newEngine = settingSearchEngine.value;
    currentSettings.searchEngine = newEngine;
    if (window.privateBrowser) {
      await window.privateBrowser.saveSettings({ searchEngine: newEngine });
    }
  });
});
