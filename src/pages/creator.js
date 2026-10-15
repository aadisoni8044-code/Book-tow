import { getCreatorProfile } from '../services/profile-service.js';
import { getUserUploads } from '../services/design-service.js';
import { renderDesignGrid } from '../components/design-grid.js';

export async function renderCreatorPage(container, searchParams) {
  const creatorId = searchParams.get('id') || 'creator_1';

  container.innerHTML = `<div class="container py-12 text-center"><i class="fa-solid fa-spinner fa-spin fa-2x text-indigo-600"></i></div>`;

  const profile = await getCreatorProfile(creatorId);
  const uploads = await getUserUploads(creatorId);
  const approvedUploads = uploads.filter(d => d.status === 'approved');

  container.innerHTML = `
    <div class="container py-8">
      <div style="background-color: var(--bg-card); border-radius: var(--radius-lg); border: 1px solid var(--border-color); padding: 2.5rem; margin-bottom: 2.5rem; display:flex; gap:2rem; align-items:center;">
        <img src="${profile.photoURL}" style="width:110px; height:110px; border-radius:9999px; object-fit:cover; border:4px solid var(--color-primary-light);">
        <div>
          <h1 style="font-size:2rem; font-weight:800; color:var(--color-secondary);">${profile.displayName}</h1>
          <p class="text-muted" style="font-size:1rem; margin-bottom:0.75rem;">${profile.bio || 'UI/UX Designer & Creator'}</p>
          <div style="display:flex; gap:1.5rem; font-size:0.875rem; color:var(--text-muted);">
            <span><i class="fa-solid fa-location-dot"></i> ${profile.location || 'Global'}</span>
            <span><i class="fa-solid fa-calendar"></i> Joined ${profile.joinedAt || '2024'}</span>
            <span><i class="fa-solid fa-layer-group"></i> ${approvedUploads.length} Published Templates</span>
          </div>
        </div>
      </div>

      <h2 style="font-size: 1.5rem; font-weight: 800; margin-bottom: 1.5rem;">Published Designs</h2>
      <div id="creator-grid-mount"></div>
    </div>
  `;

  const gridMount = container.querySelector('#creator-grid-mount');
  renderDesignGrid(gridMount, approvedUploads, false);
}
