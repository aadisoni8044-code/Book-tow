import { getCurrentUser } from '../services/auth-service.js';
import { getPendingSubmissions } from '../services/design-service.js';

export async function renderAdminPage(container) {
  const user = getCurrentUser();

  if (!user || !user.isAdmin) {
    container.innerHTML = `
      <div class="container py-12 text-center" style="max-width:500px;">
        <i class="fa-solid fa-shield-halved" style="font-size:3rem; color:var(--color-danger); margin-bottom:1rem;"></i>
        <h2 style="font-size:1.75rem; font-weight:800;">Access Denied</h2>
        <p class="text-muted" style="margin-bottom:1.5rem;">Administrative credentials and trusted backend validation are required for this section.</p>
        <a href="/" data-link class="btn btn-primary">Return to Home</a>
      </div>
    `;
    return;
  }

  const pending = await getPendingSubmissions();

  container.innerHTML = `
    <div class="container py-8">
      <div style="margin-bottom:2rem;">
        <h1 style="font-size:2.25rem; font-weight:800; color:var(--color-secondary);">Admin Moderation Portal</h1>
        <p class="text-muted">Review incoming community submissions and grant platform approval.</p>
      </div>

      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon" style="background:#FFFBEB; color:#F59E0B;"><i class="fa-solid fa-clock"></i></div>
          <div>
            <div class="stat-value">${pending.length}</div>
            <div class="stat-label">Pending Reviews</div>
          </div>
        </div>
      </div>

      <div style="background-color:var(--bg-card); border-radius:var(--radius-lg); border:1px solid var(--border-color); padding:1.5rem;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.25rem;">
          <h2 style="font-size:1.25rem; font-weight:700;">Moderation Queue</h2>
          <a href="/review-submissions" data-link class="btn btn-primary btn-sm">Launch Review Queue</a>
        </div>
        <p class="text-muted" style="font-size:0.9rem;">Click Launch Review Queue to inspect uploaded code packages, images, and grant approval.</p>
      </div>
    </div>
  `;
}
