import { getCurrentUser } from '../services/auth-service.js';
import { getUserUploads } from '../services/design-service.js';
import { updateProfile } from '../services/profile-service.js';
import { showNotification } from '../utils/dom.js';

export async function renderDashboardPage(container) {
  const user = getCurrentUser();

  if (!user) {
    window.location.href = '/sign-in';
    return;
  }

  const uploads = await getUserUploads(user.uid);
  const approvedCount = uploads.filter(d => d.status === 'approved').length;
  const pendingCount = uploads.filter(d => d.status === 'pending').length;

  container.innerHTML = `
    <div class="container py-8">
      <div class="dashboard-header">
        <div>
          <h1 style="font-size:2.25rem; font-weight:800; color:var(--color-secondary);">Creator Dashboard</h1>
          <p class="text-muted">Manage your profile, published templates, and submission status.</p>
        </div>
        <a href="/upload" data-link class="btn btn-primary"><i class="fa-solid fa-plus"></i> Upload New Design</a>
      </div>

      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon"><i class="fa-solid fa-layer-group"></i></div>
          <div>
            <div class="stat-value">${uploads.length}</div>
            <div class="stat-label">Total Submissions</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon" style="background:#ECFDF5; color:#10B981;"><i class="fa-solid fa-circle-check"></i></div>
          <div>
            <div class="stat-value">${approvedCount}</div>
            <div class="stat-label">Published Live</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon" style="background:#FFFBEB; color:#F59E0B;"><i class="fa-solid fa-clock"></i></div>
          <div>
            <div class="stat-value">${pendingCount}</div>
            <div class="stat-label">Pending Approval</div>
          </div>
        </div>
      </div>

      <div style="display:grid; grid-template-columns: 2fr 1fr; gap:2rem;">
        <div style="background-color:var(--bg-card); border-radius:var(--radius-lg); border:1px solid var(--border-color); padding:1.5rem;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
            <h2 style="font-size:1.25rem; font-weight:700;">My Recent Uploads</h2>
            <a href="/my-uploads" data-link class="btn btn-outline btn-sm">View All</a>
          </div>

          ${uploads.length === 0 ? `
            <div class="text-center py-8 text-muted">
              <p>You haven't uploaded any login screen designs yet.</p>
              <a href="/upload" data-link class="btn btn-primary btn-sm mt-4">Upload First Design</a>
            </div>
          ` : `
            <div class="data-table-container">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Preview</th>
                    <th>Title</th>
                    <th>Category</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  ${uploads.slice(0, 5).map(item => `
                    <tr>
                      <td><img src="${item.previewImage}" class="table-thumb"></td>
                      <td style="font-weight:700;"><a href="/design?id=${item.id}" data-link>${item.title}</a></td>
                      <td><span class="badge badge-primary">${item.category}</span></td>
                      <td>
                        <span class="badge ${item.status === 'approved' ? 'badge-success' : 'badge-warning'}">
                          ${item.status}
                        </span>
                      </td>
                    </tr>
                  `).join('')}
                </tbody>
              </table>
            </div>
          `}
        </div>

        <!-- Profile Card & Settings -->
        <div style="background-color:var(--bg-card); border-radius:var(--radius-lg); border:1px solid var(--border-color); padding:1.5rem;">
          <h2 style="font-size:1.25rem; font-weight:700; margin-bottom:1rem;">Profile Settings</h2>
          <form id="profile-form">
            <div class="form-group">
              <label class="form-label">Display Name</label>
              <input type="text" name="displayName" class="form-input" value="${user.displayName || ''}">
            </div>
            <div class="form-group">
              <label class="form-label">Email Address</label>
              <input type="email" class="form-input" value="${user.email}" disabled style="background:var(--bg-subtle);">
            </div>
            <button type="submit" class="btn btn-primary btn-sm" style="width:100%;">Save Profile</button>
          </form>
        </div>
      </div>
    </div>
  `;

  const profileForm = container.querySelector('#profile-form');
  profileForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const newName = profileForm.displayName.value.trim();
    await updateProfile(user.uid, { displayName: newName });
    showNotification('Profile updated successfully!', 'success');
  });
}
