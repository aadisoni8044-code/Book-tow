const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('privateBrowser', {
  getSessionInfo: () => ipcRenderer.invoke('get-session-info'),
  getSettings: () => ipcRenderer.invoke('get-settings'),
  saveSettings: (settings) => ipcRenderer.invoke('save-settings', settings),
  onThemeChanged: (callback) => ipcRenderer.on('theme-changed', (event, theme) => callback(theme)),
  clearSessionNow: () => ipcRenderer.invoke('clear-session-now'),
  getAppVersion: () => ipcRenderer.invoke('get-app-version')
});
