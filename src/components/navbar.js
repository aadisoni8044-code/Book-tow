import { getCurrentUser, signOutUser } from '../services/auth-service.js';

export function renderNavbar() {
  const container = document.getElementById('navbar-container');
  if (!container) return;

  const user = getCurrentUser();

  container.innerHTML = `
    <div class="container navbar-inner">
      <a href="/" data-link class="brand-logo">
        <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect width="64" height="64" rx="16" fill="url(#brand-grad)"/>
          <rect x="18" y="14" width="28" height="36" rx="6" fill="#FFFFFF" fill-opacity="0.95"/>
          <circle cx="32" cy="28" r="5" fill="#4F46E5"/>
          <path d="M26 40 C26 35 38 35 38 40" stroke="#4F46E5" stroke-width="3" stroke-linecap="round"/>
          <defs>
            <linearGradient id="brand-grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#4F46E5"/>
              <stop offset="100%" stop-color="#7C3AED"/>
            </linearGradient>
          </defs>
        </svg>
        <span>LoginScreen<span style="color:var(--color-primary);">.io</span></span>
      </a>

      <ul class="nav-links">
        <li><a href="/explore" data-link class="nav-link ${location.pathname === '/explore' ? 'active' : ''}">Explore</a></li>
        <li><a href="/upload" data-link class="nav-link ${location.pathname === '/upload' ? 'active' : ''}">Upload Design</a></li>
        ${user?.isAdmin ? `<li><a href="/review-submissions" data-link class="nav-link ${location.pathname === '/review-submissions' ? 'active' : ''}">Review Submissions</a></li>` : ''}
      </ul>

      <div class="nav-actions">
        ${user ? `
          <a href="/dashboard" data-link class="btn btn-secondary btn-sm">
            <img src="${user.photoURL}" class="avatar-sm" alt="${user.displayName}">
            <span>${user.displayName}</span>
          </a>
          <button id="btn-signout" class="btn btn-outline btn-sm">Sign Out</button>
        ` : `
          <a href="/sign-in" data-link class="btn btn-primary btn-sm">Sign In</a>
        `}
      </div>
    </div>
  `;

  const btnSignout = container.querySelector('#btn-signout');
  if (btnSignout) {
    btnSignout.addEventListener('click', async () => {
      await signOutUser();
      window.location.href = '/';
    });
  }
}
