import { getCurrentUser } from '../services/auth-service.js';
import { getUserUploads } from '../services/design-service.js';

export async function renderMyUploadsPage(container) {
  const user = getCurrentUser();

  if (!user) {
    window.location.href = '/sign-in';
    return;
  }

  const uploads = await getUserUploads(user.uid);

  container.innerHTML = `
    <div class="container py-8">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:2rem;">
        <div>
          <h1 style="font-size:2.25rem; font-weight:800; color:var(--color-secondary);">My Submissions</h1>
          <p class="text-muted">Track moderation status and manage your uploaded templates.</p>
        </div>
        <a href="/upload" data-link class="btn btn-primary"><i class="fa-solid fa-plus"></i> Upload Design</a>
      </div>

      <div class="data-table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Template Preview</th>
              <th>Design Title</th>
              <th>Category</th>
              <th>Submitted Date</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            ${uploads.length === 0 ? `
              <tr>
                <td colspan="6" class="text-center py-8 text-muted">
                  No submissions yet. <a href="/upload" data-link style="color:var(--color-primary);">Upload your first login screen design</a>
                </td>
              </tr>
            ` : uploads.map(item => `
              <tr>
                <td><img src="${item.previewImage}" class="table-thumb"></td>
                <td style="font-weight:700;">${item.title}</td>
                <td><span class="badge badge-primary">${item.category}</span></td>
                <td>${new Date(item.createdAt).toLocaleDateString()}</td>
                <td>
                  <span class="badge ${item.status === 'approved' ? 'badge-success' : item.status === 'rejected' ? 'badge-danger' : 'badge-warning'}">
                    ${item.status}
                  </span>
                </td>
                <td>
                  <a href="/preview?id=${item.id}" data-link class="btn btn-outline btn-sm">Preview</a>
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}
