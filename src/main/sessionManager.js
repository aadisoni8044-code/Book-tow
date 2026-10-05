const { session } = require('electron');
const crypto = require('crypto');

class SessionManager {
  constructor() {
    this.sessionId = 'temp_' + Date.now() + '_' + crypto.randomBytes(4).toString('hex');
    this.partitionName = `persist:${this.sessionId}`;
    this.currentSession = null;
  }

  /**
   * Initializes and returns the isolated temporary Electron Session.
   */
  getOrCreateSession() {
    if (!this.currentSession) {
      this.currentSession = session.fromPartition(this.partitionName, { cache: true });

      // Enforce strict privacy configurations
      this.currentSession.setPermissionRequestHandler((webContents, permission, callback) => {
        // Block geolocation, notifications, camera, microphone by default or require strict prompt
        const allowedPermissions = [];
        if (allowedPermissions.includes(permission)) {
          callback(true);
        } else {
          callback(false);
        }
      });

      // Disable spellcheck or telemetries if supported
      if (typeof this.currentSession.setSpellCheckerEnabled === 'function') {
        this.currentSession.setSpellCheckerEnabled(false);
      }
    }
    return this.currentSession;
  }

  getSessionId() {
    return this.sessionId;
  }

  getPartitionName() {
    return this.partitionName;
  }
}

module.exports = SessionManager;
