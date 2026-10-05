/**
  * Parses input text from the address bar to distinguish between valid web URLs and search queries.
  * @param {string} input - Raw text entered in address bar
  * @param {string} searchEngine - Base search engine URL template
  * @returns {string} - Full target URL
  */
function parseAddressInput(input, searchEngine = 'https://duckduckgo.com/?q=') {
  if (!input) return 'home.html';
  const trimmed = input.trim();

  // Check if internal app page
  if (trimmed === 'home.html' || trimmed === 'app://home') {
    return 'home.html';
  }

  // Regex patterns to detect domain name / valid URL vs search text
  const urlWithProtocol = /^(https?:\/\/|file:\/\/|ftp:\/\/)/i;
  const domainPattern = /^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(:\d+)?(\/.*)?$/;
  const localhostPattern = /^localhost(:\d+)?(\/.*)?$/i;
  const ipAddressPattern = /^(\d{1,3}\.){3}\d{1,3}(:\d+)?(\/.*)?$/;

  if (urlWithProtocol.test(trimmed)) {
    return trimmed;
  }

  if (domainPattern.test(trimmed) || localhostPattern.test(trimmed) || ipAddressPattern.test(trimmed)) {
    return `https://${trimmed}`;
  }

  // Otherwise, treat as search query
  return `${searchEngine}${encodeURIComponent(trimmed)}`;
}

/**
 * Checks whether an input string is recognized as a direct URL vs a search query.
 */
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

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { parseAddressInput, isDirectUrl };
}
