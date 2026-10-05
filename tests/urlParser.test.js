const test = require('node:test');
const assert = require('node:assert');
const { parseAddressInput, isDirectUrl } = require('../src/renderer/js/urlParser');

test('parseAddressInput - direct domain inputs', () => {
  assert.strictEqual(parseAddressInput('example.com'), 'https://example.com');
  assert.strictEqual(parseAddressInput('https://github.com'), 'https://github.com');
  assert.strictEqual(parseAddressInput('http://localhost:8080'), 'http://localhost:8080');
  assert.strictEqual(parseAddressInput('127.0.0.1:3000'), 'https://127.0.0.1:3000');
});

test('parseAddressInput - internal home page', () => {
  assert.strictEqual(parseAddressInput('home.html'), 'home.html');
  assert.strictEqual(parseAddressInput('app://home'), 'home.html');
  assert.strictEqual(parseAddressInput(''), 'home.html');
});

test('parseAddressInput - search queries', () => {
  const engine = 'https://duckduckgo.com/?q=';
  assert.strictEqual(
    parseAddressInput('privacy browser electron', engine),
    'https://duckduckgo.com/?q=privacy%20browser%20electron'
  );
  assert.strictEqual(
    parseAddressInput('what is 2 + 2?', engine),
    'https://duckduckgo.com/?q=what%20is%202%20%2B%202%3F'
  );
});

test('isDirectUrl helper', () => {
  assert.strictEqual(isDirectUrl('https://mozilla.org'), true);
  assert.strictEqual(isDirectUrl('wikipedia.org'), true);
  assert.strictEqual(isDirectUrl('how to implement privacy browser'), false);
  assert.strictEqual(isDirectUrl('hello world'), false);
});
