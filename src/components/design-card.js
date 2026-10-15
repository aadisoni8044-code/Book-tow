import { formatDate, formatNumber } from '../utils/formatting.js';

export function createDesignCard(design) {
  const card = document.createElement('div');
  card.className = 'design-card';

  card.innerHTML = `
    <div class="card-media">
      <img src="${design.previewImage}" alt="${design.title}" loading="lazy">
      <div class="card-overlay">
        <div class="overlay-actions">
          <a href="/preview?id=${design.id}" data-link class="btn btn-primary btn-sm" style="flex:1;">
            <i class="fa-solid fa-eye"></i> Live Preview
          </a>
          <a href="/design?id=${design.id}" data-link class="btn btn-secondary btn-sm">
            <i class="fa-solid fa-circle-info"></i> Details
          </a>
        </div>
      </div>
    </div>

    <div class="card-body">
      <h3 class="card-title">
        <a href="/design?id=${design.id}" data-link>${design.title}</a>
      </h3>

      <div class="card-creator">
        <a href="/creator?id=${design.creatorId}" data-link style="display:flex; align-items:center; gap:0.5rem;">
          <img src="${design.creatorAvatar}" class="avatar-sm" alt="${design.creatorName}">
          <span>${design.creatorName}</span>
        </a>
      </div>

      <div class="card-footer-info">
        <span class="badge badge-primary">${design.category || 'UI Screen'}</span>
        <div style="display:flex; gap:0.75rem;">
          <span><i class="fa-solid fa-eye"></i> ${formatNumber(design.views || 0)}</span>
          <span><i class="fa-solid fa-download"></i> ${formatNumber(design.downloads || 0)}</span>
        </div>
      </div>
    </div>
  `;

  return card;
}
