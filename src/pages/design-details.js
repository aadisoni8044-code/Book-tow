import { getDesignById } from '../services/design-service.js';
import { downloadDesignPackage } from '../services/download-service.js';
import { formatDate, formatNumber } from '../utils/formatting.js';
import { showNotification } from '../utils/dom.js';

export async function renderDesignDetailsPage(container, searchParams) {
  const designId = searchParams.get('id');
  if (!designId) {
    container.innerHTML = `<div class="container py-12 text-center"><h3>Invalid Design ID</h3></div>`;
    return;
  }

  container.innerHTML = `<div class="container py-12 text-center"><i class="fa-solid fa-spinner fa-spin fa-2x text-indigo-600"></i></div>`;

  const design = await getDesignById(designId);
  if (!design) {
    container.innerHTML = `
      <div class="container py-12 text-center">
        <h2>Design Not Found</h2>
        <a href="/explore" data-link class="btn btn-primary mt-4">Back to Gallery</a>
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <div class="container py-8">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 1.5rem;">
        <div>
          <span class="badge badge-primary mb-2">${design.category || 'UI Component'}</span>
          <h1 style="font-size: 2.25rem; font-weight: 800; color: var(--color-secondary);">${design.title}</h1>
        </div>
        <div style="display:flex; gap:1rem;">
          <a href="/preview?id=${design.id}" data-link class="btn btn-primary">
            <i class="fa-solid fa-play"></i> Live Preview
          </a>
          <button id="btn-download-design" class="btn btn-secondary">
            <i class="fa-solid fa-download"></i> Download Template
          </button>
        </div>
      </div>

      <div style="display:grid; grid-template-columns: 2.5fr 1fr; gap: 2rem; margin-bottom: 3rem;">
        <div style="background-color: var(--bg-card); border-radius: var(--radius-lg); border: 1px solid var(--border-color); overflow: hidden; box-shadow: var(--shadow-md);">
          <img src="${design.previewImage}" alt="${design.title}" style="width:100%; object-fit:cover;">
        </div>

        <div>
          <div style="background-color: var(--bg-card); border-radius: var(--radius-lg); border: 1px solid var(--border-color); padding: 1.5rem; margin-bottom: 1.5rem;">
            <h3 style="font-size:1.1rem; font-weight:700; margin-bottom:1rem;">Created By</h3>
            <div style="display:flex; align-items:center; gap:0.875rem; margin-bottom:1.25rem;">
              <img src="${design.creatorAvatar}" style="width:48px; height:48px; border-radius:9999px; object-fit:cover;">
              <div>
                <a href="/creator?id=${design.creatorId}" data-link style="font-weight:700; color:var(--text-main);">${design.creatorName}</a>
                <p class="text-muted" style="font-size:0.825rem;">UI/UX Creator</p>
              </div>
            </div>
            <a href="/creator?id=${design.creatorId}" data-link class="btn btn-outline btn-sm" style="width:100%;">View Creator Profile</a>
          </div>

          <div style="background-color: var(--bg-card); border-radius: var(--radius-lg); border: 1px solid var(--border-color); padding: 1.5rem;">
            <h3 style="font-size:1.1rem; font-weight:700; margin-bottom:1rem;">Design Stats</h3>
            <div style="display:flex; flex-direction:column; gap:0.75rem; font-size:0.9rem;">
              <div style="display:flex; justify-content:space-between;">
                <span class="text-muted">Status</span>
                <span class="badge ${design.status === 'approved' ? 'badge-success' : 'badge-warning'}">${design.status}</span>
              </div>
              <div style="display:flex; justify-content:space-between;">
                <span class="text-muted">Views</span>
                <span style="font-weight:600;">${formatNumber(design.views || 0)}</span>
              </div>
              <div style="display:flex; justify-content:space-between;">
                <span class="text-muted">Downloads</span>
                <span style="font-weight:600;">${formatNumber(design.downloads || 0)}</span>
              </div>
              <div style="display:flex; justify-content:space-between;">
                <span class="text-muted">Published Date</span>
                <span style="font-weight:600;">${formatDate(design.createdAt)}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div style="background-color: var(--bg-card); border-radius: var(--radius-lg); border: 1px solid var(--border-color); padding: 2rem;">
        <h2 style="font-size: 1.35rem; font-weight: 700; margin-bottom: 1rem;">Description</h2>
        <p style="color: var(--text-muted); font-size: 1rem; line-height: 1.6; margin-bottom: 1.5rem;">
          ${design.description}
        </p>
        <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
          ${(design.tags || []).map(t => `<span class="badge badge-primary">#${t}</span>`).join('')}
        </div>
      </div>
    </div>
  `;

  const btnDownload = container.querySelector('#btn-download-design');
  if (btnDownload) {
    btnDownload.addEventListener('click', async () => {
      try {
        await downloadDesignPackage(design);
        showNotification('Template download started!', 'success');
      } catch (err) {
        showNotification(err.message, 'danger');
      }
    });
  }
}
