import { getCurrentUser } from '../services/auth-service.js';
import { getPendingSubmissions } from '../services/design-service.js';
import { updateSubmissionStatus } from '../services/upload-service.js';
import { showNotification } from '../utils/dom.js';

export async function renderReviewSubmissionsPage(container) {
  const user = getCurrentUser();

  if (!user || !user.isAdmin) {
    container.innerHTML = `
      <div class="container py-12 text-center" style="max-width:500px;">
        <i class="fa-solid fa-shield-halved" style="font-size:3rem; color:var(--color-danger); margin-bottom:1rem;"></i>
        <h2 style="font-size:1.75rem; font-weight:800;">Access Restricted</h2>
        <p class="text-muted" style="margin-bottom:1.5rem;">Only verified platform administrators may access submission moderation.</p>
        <a href="/" data-link class="btn btn-primary">Return Home</a>
      </div>
    `;
    return;
  }

  container.innerHTML = `<div class="container py-12 text-center"><i class="fa-solid fa-spinner fa-spin fa-2x text-indigo-600"></i></div>`;

  const pending = await getPendingSubmissions();

  container.innerHTML = `
    <div class="container py-8">
      <div style="margin-bottom:2rem;">
        <h1 style="font-size:2.25rem; font-weight:800; color:var(--color-secondary);">Review Submissions</h1>
        <p class="text-muted">Approve or reject pending community login templates.</p>
      </div>

      ${pending.length === 0 ? `
        <div class="text-center py-12" style="background:var(--bg-card); border-radius:var(--radius-lg); border:1px solid var(--border-color);">
          <i class="fa-solid fa-circle-check" style="font-size:3rem; color:var(--color-success); margin-bottom:1rem;"></i>
          <h3 style="font-size:1.25rem; font-weight:700;">Moderation Queue Empty</h3>
          <p class="text-muted">All submitted designs have been reviewed and processed.</p>
        </div>
      ` : `
        <div style="display:flex; flex-direction:column; gap:1.5rem;">
          ${pending.map(item => `
            <div class="review-card" data-id="${item.id}" style="background-color:var(--bg-card); border-radius:var(--radius-lg); border:1px solid var(--border-color); padding:1.5rem; display:grid; grid-template-columns: 200px 1fr auto; gap:1.5rem; align-items:center;">
              <img src="${item.previewImage}" style="width:200px; height:130px; object-fit:cover; border-radius:var(--radius-md);">
              <div>
                <span class="badge badge-warning mb-2">Pending Review</span>
                <h3 style="font-size:1.25rem; font-weight:700;">${item.title}</h3>
                <p class="text-muted" style="font-size:0.875rem; margin-bottom:0.5rem;">Submitted by <strong>${item.creatorName}</strong> on ${new Date(item.createdAt).toLocaleDateString()}</p>
                <p style="font-size:0.9rem; color:var(--text-main);">${item.description}</p>
              </div>
              <div style="display:flex; flex-direction:column; gap:0.5rem; min-width:140px;">
                <a href="/preview?id=${item.id}" data-link class="btn btn-outline btn-sm"><i class="fa-solid fa-eye"></i> Inspect Code</a>
                <button class="btn btn-primary btn-sm btn-approve" data-id="${item.id}"><i class="fa-solid fa-check"></i> Approve</button>
                <button class="btn btn-secondary btn-sm btn-reject" data-id="${item.id}" style="color:var(--color-danger);"><i class="fa-solid fa-xmark"></i> Reject</button>
              </div>
            </div>
          `).join('')}
        </div>
      `}
    </div>
  `;

  container.querySelectorAll('.btn-approve').forEach(btn => {
    btn.addEventListener('click', async () => {
      const id = btn.dataset.id;
      btn.disabled = true;
      await updateSubmissionStatus(id, 'approved');
      showNotification('Design approved! Published to live gallery.', 'success');
      btn.closest('.review-card').remove();
    });
  });

  container.querySelectorAll('.btn-reject').forEach(btn => {
    btn.addEventListener('click', async () => {
      const id = btn.dataset.id;
      btn.disabled = true;
      await updateSubmissionStatus(id, 'rejected');
      showNotification('Design rejected.', 'warning');
      btn.closest('.review-card').remove();
    });
  });
}
