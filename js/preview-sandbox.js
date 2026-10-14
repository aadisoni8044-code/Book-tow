// Secure Live Preview Sandbox & Download Engine
export class PreviewSandboxEngine {
  /**
   * Generates a isolated Blob URL with sandboxed HTML execution capabilities.
   * Safety Features:
   * - Restrictive CSP Content-Security-Policy header metatag inside iframe.
   * - Sandboxed without 'allow-same-origin' to prevent host cookie, token, or localStorage access.
   * - No parent frame object access.
   */
  static createSafeIframeDocument(htmlCode, cssCode = '', jsCode = '') {
    const safeContent = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self' 'unsafe-inline' data: blob: https://fonts.googleapis.com https://fonts.gstatic.com https://cdnjs.cloudflare.com; script-src 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; img-src 'self' data: https: blob:; connect-src 'none';">
  <style>
    /* Reset & Clean Sandboxed Base Rules */
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; min-height: 100vh; overflow-x: hidden; }
    ${cssCode}
  </style>
</head>
<body>
  ${htmlCode}
  <script>
    // Security Restriction Guards inside Iframe
    (function() {
      try {
        window.localStorage = undefined;
        window.sessionStorage = undefined;
        window.indexedDB = undefined;
      } catch (e) {}
    })();
    ${jsCode}
  </script>
</body>
</html>
    `;

    const blob = new Blob([safeContent], { type: 'text/html;charset=utf-8' });
    return URL.createObjectURL(blob);
  }

  /**
   * Configures an existing HTMLIFrameElement with maximum security attributes
   */
  static applySandboxRestrictions(iframeElement) {
    if (!iframeElement) return;
    // Allow scripts and forms for interactive login simulation, but strictly forbid same-origin access, popups, or top navigation
    iframeElement.setAttribute('sandbox', 'allow-scripts allow-forms');
    iframeElement.setAttribute('referrerpolicy', 'no-referrer');
  }

  /**
   * Client File Validation Rules
   */
  static validateUploadFile(file, allowedTypes, maxSizeBytes) {
    if (!file) return { valid: false, error: 'No file selected.' };

    const extension = file.name.split('.').pop().toLowerCase();
    const isValidType = allowedTypes.includes(extension) || allowedTypes.includes(file.type);

    if (!isValidType) {
      return {
        valid: false,
        error: `Invalid file format .${extension}. Permitted extensions: ${allowedTypes.join(', ')}`
      };
    }

    if (file.size > maxSizeBytes) {
      const maxMb = (maxSizeBytes / (1024 * 1024)).toFixed(1);
      return {
        valid: false,
        error: `File size exceeds the limit of ${maxMb}MB.`
      };
    }

    return { valid: true };
  }

  /**
   * Helper to trigger download of ZIP package or files safely across devices
   */
  static triggerDownload(fileUrlOrBlob, filename) {
    const link = document.createElement('a');
    link.href = fileUrlOrBlob;
    link.download = filename || 'LoginScreen-Package.zip';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}
