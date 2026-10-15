import { getDesignById } from '../services/design-service.js';
import { downloadDesignPackage } from '../services/download-service.js';
import { showNotification } from '../utils/dom.js';

export async function renderPreviewPage(container, searchParams) {
  const designId = searchParams.get('id');
  if (!designId) {
    container.innerHTML = `<div class="container py-12 text-center"><h3>Invalid Design ID</h3></div>`;
    return;
  }

  const design = await getDesignById(designId);
  if (!design) {
    container.innerHTML = `<div class="container py-12 text-center"><h2>Design Not Found</h2></div>`;
    return;
  }

  container.innerHTML = `
    <div style="display:flex; flex-direction:column; height: calc(100vh - 72px); background-color: var(--bg-dark);">
      <!-- Top Control Header Bar -->
      <div style="display:flex; justify-content:space-between; align-items:center; padding: 0.75rem 1.5rem; background-color: #0B0F19; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--text-white);">
        <div style="display:flex; align-items:center; gap: 1rem;">
          <a href="/design?id=${design.id}" data-link class="btn btn-outline btn-sm" style="color:var(--text-white); border-color:rgba(255,255,255,0.2);">
            <i class="fa-solid fa-arrow-left"></i> Details
          </a>
          <div>
            <h2 style="font-size:1.1rem; font-weight:700;">${design.title}</h2>
            <span style="font-size:0.75rem; color:#94A3B8;">Sandboxed Origin Preview</span>
          </div>
        </div>

        <div style="display:flex; gap:0.75rem;">
          <button id="btn-toggle-code" class="btn btn-secondary btn-sm">
            <i class="fa-solid fa-code"></i> View Source
          </button>
          <button id="btn-download-preview" class="btn btn-primary btn-sm">
            <i class="fa-solid fa-download"></i> Download Template
          </button>
        </div>
      </div>

      <!-- Main Sandbox View Container -->
      <div style="flex:1; display:flex; position:relative; overflow:hidden;">
        <!-- Code Drawer Panel -->
        <div id="code-drawer" style="width: 400px; background-color: #07090E; border-right: 1px solid rgba(255,255,255,0.1); display:none; flex-direction:column;">
          <div style="padding:0.75rem 1rem; background:rgba(255,255,255,0.05); color:#fff; font-size:0.85rem; font-weight:700;">
            Source HTML/CSS
          </div>
          <textarea readonly style="flex:1; background:transparent; color:#A7F3D0; border:none; padding:1rem; font-family:monospace; font-size:0.85rem; resize:none;">${escapeHtml(design.codeSnippet || '')}</textarea>
        </div>

        <!-- Appropriately Sandboxed Isolated Iframe Container -->
        <div style="flex:1; display:flex; align-items:center; justify-content:center; background-color: #1E293B; padding:1rem;">
          <iframe
            id="sandboxed-frame"
            sandbox="allow-scripts"
            csp="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline';"
            style="width: 100%; height: 100%; border: none; border-radius: var(--radius-md); background-color: #07090E; box-shadow: var(--shadow-xl);"
            title="Safe Preview"
          ></iframe>
        </div>
      </div>
    </div>
  `;

  const iframe = container.querySelector('#sandboxed-frame');
  const codeDrawer = container.querySelector('#code-drawer');
  const btnToggleCode = container.querySelector('#btn-toggle-code');
  const btnDownload = container.querySelector('#btn-download-preview');

  // Inject preview document into isolated sandboxed frame
  const htmlContent = design.codeSnippet || getFallbackPreviewHTML(design.title);
  iframe.srcdoc = htmlContent;

  btnToggleCode.addEventListener('click', () => {
    const isHidden = codeDrawer.style.display === 'none';
    codeDrawer.style.display = isHidden ? 'flex' : 'none';
  });

  btnDownload.addEventListener('click', async () => {
    try {
      await downloadDesignPackage(design);
      showNotification('Template package downloaded.', 'success');
    } catch (err) {
      showNotification(err.message, 'danger');
    }
  });
}

function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function getFallbackPreviewHTML(title) {
  return `<!DOCTYPE html>
<html>
<head>
  <style>
    body { background: #0b0f19; color: white; font-family: system-ui; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
    .card { background: rgba(255,255,255,0.05); padding: 2rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); width: 320px; }
  </style>
</head>
<body>
  <div class="card">
    <h3>${title}</h3>
    <p>Safe Preview Ready</p>
  </div>
</body>
</html>`;
}
