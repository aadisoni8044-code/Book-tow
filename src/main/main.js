const { app, BrowserWindow, ipcMain, nativeTheme } = require('electron');
const path = require('path');
const fs = require('fs');
const SessionManager = require('./sessionManager');
const CleanupManager = require('./cleanupManager');

let mainWindow = null;
let sessionManager = null;
const settingsPath = path.join(app.getPath('userData'), 'settings.json');

// Default App Settings
let appSettings = {
  theme: 'system', // 'light', 'dark', 'system'
  homePage: 'app://home',
  searchEngine: 'https://duckduckgo.com/?q='
};

function loadSettings() {
  try {
    if (fs.existsSync(settingsPath)) {
      const data = fs.readFileSync(settingsPath, 'utf8');
      appSettings = { ...appSettings, ...JSON.parse(data) };
    }
  } catch (err) {
    console.error('[Main] Failed to load settings:', err);
  }
}

function saveSettings(newSettings) {
  try {
    appSettings = { ...appSettings, ...newSettings };
    fs.writeFileSync(settingsPath, JSON.stringify(appSettings, null, 2), 'utf8');
  } catch (err) {
    console.error('[Main] Failed to save settings:', err);
  }
}

function createWindow() {
  sessionManager = new SessionManager();
  const tempSession = sessionManager.getOrCreateSession();

  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    title: 'Private Browser',
    backgroundColor: '#0f172a',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      webviewTag: true,
      session: tempSession
    }
  });

  mainWindow.setMenuBarVisibility(false);

  // Load the main shell UI
  mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'));

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// Ensure single instance or clean startup
app.whenReady().then(async () => {
  // Purge any previous residual temporary sessions on startup
  CleanupManager.cleanOldSessions();

  loadSettings();

  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', async () => {
  if (sessionManager && sessionManager.currentSession) {
    await CleanupManager.clearSessionData(sessionManager.currentSession);
  }
  CleanupManager.cleanOldSessions();
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// IPC Communications
ipcMain.handle('get-session-info', () => {
  return {
    sessionId: sessionManager ? sessionManager.getSessionId() : 'active',
    partition: sessionManager ? sessionManager.getPartitionName() : 'temp',
    isTemporary: true,
    cookies: 'Temporary',
    history: 'Not saved',
    cache: 'Temporary',
    localStorage: 'Temporary',
    sessionData: 'Cleared when browser closes'
  };
});

ipcMain.handle('get-settings', () => {
  return appSettings;
});

ipcMain.handle('save-settings', (event, newSettings) => {
  saveSettings(newSettings);
  if (newSettings.theme) {
    if (newSettings.theme === 'dark') nativeTheme.themeSource = 'dark';
    else if (newSettings.theme === 'light') nativeTheme.themeSource = 'light';
    else nativeTheme.themeSource = 'system';
  }
  return appSettings;
});

ipcMain.handle('clear-session-now', async () => {
  if (sessionManager && sessionManager.currentSession) {
    await CleanupManager.clearSessionData(sessionManager.currentSession);
  }
  return true;
});

ipcMain.handle('get-app-version', () => {
  return app.getVersion();
});
