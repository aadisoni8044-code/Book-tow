import test from 'node:test';
import assert from 'node:assert/strict';

function canAccessPendingSubmissions(user) {
  return Boolean(user && user.isAdmin);
}

function canApproveSubmission(user, submission) {
  if (!user || !user.isAdmin) return false;
  // Ordinary users cannot approve their own or any submissions
  return true;
}

test('ordinary user cannot access pending submissions queue', () => {
  const normalUser = { uid: 'u1', email: 'user@domain.com', isAdmin: false };
  assert.equal(canAccessPendingSubmissions(normalUser), false);
});

test('admin user can access pending submissions queue', () => {
  const adminUser = { uid: 'a1', email: 'admin@admin.com', isAdmin: true };
  assert.equal(canAccessPendingSubmissions(adminUser), true);
});

test('only admin users can perform submission approval action', () => {
  const normalUser = { uid: 'u1', email: 'user@domain.com', isAdmin: false };
  const adminUser = { uid: 'a1', email: 'admin@admin.com', isAdmin: true };
  const submission = { id: 's1', creatorId: 'u1', status: 'pending' };

  assert.equal(canApproveSubmission(normalUser, submission), false);
  assert.equal(canApproveSubmission(adminUser, submission), true);
});
