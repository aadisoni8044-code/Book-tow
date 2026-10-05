const test = require('node:test');
const assert = require('node:assert');
const SessionManager = require('../src/main/sessionManager');
const CleanupManager = require('../src/main/cleanupManager');

test('SessionManager - unique partition generator', () => {
  const sm1 = new SessionManager();
  const sm2 = new SessionManager();

  assert.ok(sm1.getSessionId().startsWith('temp_'));
  assert.ok(sm2.getSessionId().startsWith('temp_'));
  assert.notStrictEqual(sm1.getSessionId(), sm2.getSessionId());
  assert.strictEqual(sm1.getPartitionName(), `persist:${sm1.getSessionId()}`);
});

test('CleanupManager - static interface exists', () => {
  assert.strictEqual(typeof CleanupManager.cleanOldSessions, 'function');
  assert.strictEqual(typeof CleanupManager.clearSessionData, 'function');
});
