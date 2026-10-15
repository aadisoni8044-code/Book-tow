import test from 'node:test';
import assert from 'node:assert/strict';
import { validateEmail, validatePassword, validateSubmission } from '../src/utils/validation.js';

test('validateEmail checks valid and invalid email addresses', () => {
  assert.equal(validateEmail('creator@domain.com'), true);
  assert.equal(validateEmail('invalid-email'), false);
  assert.equal(validateEmail(''), false);
});

test('validatePassword checks minimum length threshold', () => {
  assert.equal(validatePassword('123456'), true);
  assert.equal(validatePassword('12345'), false);
  assert.equal(validatePassword(''), false);
});

test('validateSubmission flags missing or short titles and descriptions', () => {
  const invalidResult = validateSubmission({
    title: 'ab',
    category: '',
    description: 'short'
  });

  assert.equal(invalidResult.isValid, false);
  assert.ok(invalidResult.errors.title);
  assert.ok(invalidResult.errors.category);
  assert.ok(invalidResult.errors.description);

  const validResult = validateSubmission({
    title: 'VisionOS Spatial Login Screen UI',
    category: 'Glassmorphism',
    description: 'Comprehensive glassmorphic authentication layout with particle canvas.'
  });

  assert.equal(validResult.isValid, true);
});
