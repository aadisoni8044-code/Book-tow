const fs = require('fs');
const path = require('path');
const { app } = require('electron');

class CleanupManager {
  /**
   * Cleans up orphaned or lingering temporary partition folders in app userData directory.
   */
  static cleanOldSessions() {
    try {
      const userDataPath = app.getPath('userData');
      const partitionsPath = path.join(userDataPath, 'Partitions');

      if (fs.existsSync(partitionsPath)) {
        const entries = fs.readdirSync(partitionsPath);
        for (const entry of entries) {
          if (entry.startsWith('temp_')) {
            const fullPath = path.join(partitionsPath, entry);
            try {
              fs.rmSync(fullPath, { recursive: true, force: true });
            } catch (err) {
              console.warn(`[CleanupManager] Could not delete old session folder ${entry}:`, err.message);
            }
          }
        }
      }
    } catch (err) {
      console.error('[CleanupManager] Error during cleanup of old sessions:', err);
    }
  }

  /**
   * Clears storage data for a specific session object.
   */
  static async clearSessionData(targetSession) {
    if (!targetSession) return;
    try {
      await targetSession.clearStorageData({
        storages: [
          'appcache',
          'cookies',
          'filesystem',
          'indexdb',
          'localstorage',
          'shadercache',
          'websql',
          'serviceworkers',
          'cachestorage'
        ]
      });
      await targetSession.clearCache();
      await targetSession.clearAuthCache();
      await targetSession.clearCodeCaches({});
    } catch (err) {
      console.error('[CleanupManager] Error clearing session storage data:', err);
    }
  }
}

module.exports = CleanupManager;
