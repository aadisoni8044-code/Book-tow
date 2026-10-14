// Toast Notification Helper
export function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;

  let iconHtml = 'ℹ️';
  if (type === 'success') iconHtml = '✅';
  if (type === 'error') iconHtml = '❌';

  toast.innerHTML = `<span>${iconHtml}</span> <span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// Navigation and Common UI Controls Setup
export function initCommonUI(authService) {
  // Mobile Hamburger Menu Toggle
  const mobileBtn = document.querySelector('.mobile-menu-btn');
  const navLinks = document.querySelector('.nav-links');

  if (mobileBtn && navLinks) {
    mobileBtn.addEventListener('click', () => {
      navLinks.classList.toggle('active');
    });
  }

  // Inject Sign In / Register Modal HTML if not present
  if (!document.getElementById('auth-modal')) {
    const modalMarkup = `
      <div id="auth-modal" class="modal-overlay">
        <div class="modal-container">
          <button class="modal-close" id="auth-modal-close">&times;</button>

          <div id="auth-tab-nav" style="display: flex; gap: 1rem; margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-glass); padding-bottom: 0.75rem;">
            <button id="tab-login-btn" class="btn btn-sm btn-primary" style="flex: 1;">Sign In</button>
            <button id="tab-register-btn" class="btn btn-sm btn-secondary" style="flex: 1;">Create Account</button>
          </div>

          <!-- Sign In Form -->
          <form id="signin-form">
            <h3 style="margin-bottom: 1rem; color: #fff;">Welcome Back</h3>
            <div class="form-group">
              <label class="form-label">Email Address</label>
              <input type="email" id="login-email" class="form-input" placeholder="you@example.com" required />
            </div>
            <div class="form-group">
              <label class="form-label">Password</label>
              <input type="password" id="login-password" class="form-input" placeholder="••••••••" required />
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 0.5rem;">Sign In</button>
          </form>

          <!-- Register Form -->
          <form id="register-form" style="display: none;">
            <h3 style="margin-bottom: 1rem; color: #fff;">Join Community</h3>
            <div class="form-group">
              <label class="form-label">Full Name / Creator Handle</label>
              <input type="text" id="reg-name" class="form-input" placeholder="e.g. Alex Rivera" required />
            </div>
            <div class="form-group">
              <label class="form-label">Email Address</label>
              <input type="email" id="reg-email" class="form-input" placeholder="you@example.com" required />
            </div>
            <div class="form-group">
              <label class="form-label">Password (min 6 characters)</label>
              <input type="password" id="reg-password" class="form-input" placeholder="••••••••" minlength="6" required />
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 0.5rem;">Create Account</button>
          </form>
        </div>
      </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalMarkup);
  }

  // Modal tab toggles
  const authModal = document.getElementById('auth-modal');
  const closeBtn = document.getElementById('auth-modal-close');
  const tabLogin = document.getElementById('tab-login-btn');
  const tabRegister = document.getElementById('tab-register-btn');
  const formLogin = document.getElementById('signin-form');
  const formRegister = document.getElementById('register-form');

  if (tabLogin && tabRegister) {
    tabLogin.addEventListener('click', () => {
      tabLogin.className = 'btn btn-sm btn-primary';
      tabRegister.className = 'btn btn-sm btn-secondary';
      formLogin.style.display = 'block';
      formRegister.style.display = 'none';
    });

    tabRegister.addEventListener('click', () => {
      tabRegister.className = 'btn btn-sm btn-primary';
      tabLogin.className = 'btn btn-sm btn-secondary';
      formLogin.style.display = 'none';
      formRegister.style.display = 'block';
    });
  }

  if (closeBtn && authModal) {
    closeBtn.addEventListener('click', () => {
      authModal.classList.remove('active');
    });
    authModal.addEventListener('click', (e) => {
      if (e.target === authModal) authModal.classList.remove('active');
    });
  }

  // Handlers for Form Submissions
  if (formLogin) {
    formLogin.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('login-email').value.trim();
      const pass = document.getElementById('login-password').value;
      try {
        await authService.signIn(email, pass);
        showToast('Signed in successfully!', 'success');
        authModal.classList.remove('active');
      } catch (err) {
        showToast(err.message || 'Failed to sign in', 'error');
      }
    });
  }

  if (formRegister) {
    formRegister.addEventListener('submit', async (e) => {
      e.preventDefault();
      const name = document.getElementById('reg-name').value.trim();
      const email = document.getElementById('reg-email').value.trim();
      const pass = document.getElementById('reg-password').value;
      try {
        await authService.signUp(email, pass, name);
        showToast('Account created successfully!', 'success');
        authModal.classList.remove('active');
      } catch (err) {
        showToast(err.message || 'Failed to create account', 'error');
      }
    });
  }

  // Subscribe to Auth State Changes to Update UI Navigation Bar
  authService.onAuthChange((user) => {
    const navActions = document.querySelector('.nav-actions');
    if (!navActions) return;

    if (user) {
      const initial = user.displayName ? user.displayName.charAt(0).toUpperCase() : 'U';
      navActions.innerHTML = `
        <div class="user-menu-wrapper">
          <button class="user-avatar-btn" id="user-avatar-trigger" title="${user.displayName}">
            ${initial}
          </button>
          <div class="user-dropdown" id="user-dropdown-menu">
            <div class="user-dropdown-header">
              <div class="user-dropdown-name">${user.displayName}</div>
              <div class="user-dropdown-email">${user.email}</div>
            </div>
            <a href="profile.html" class="dropdown-item">👤 My Profile & Uploads</a>
            <a href="upload.html" class="dropdown-item">📤 Upload Design</a>
            ${user.isAdmin ? '<a href="admin.html" class="dropdown-item" style="color: var(--accent-amber);">🛡️ Admin Panel</a>' : ''}
            <a href="#" id="sign-out-btn" class="dropdown-item" style="color: var(--accent-pink);">🚪 Sign Out</a>
          </div>
        </div>
      `;

      const avatarTrigger = document.getElementById('user-avatar-trigger');
      const dropdownMenu = document.getElementById('user-dropdown-menu');
      const signOutBtn = document.getElementById('sign-out-btn');

      if (avatarTrigger && dropdownMenu) {
        avatarTrigger.addEventListener('click', (e) => {
          e.stopPropagation();
          dropdownMenu.classList.toggle('show');
        });
        document.addEventListener('click', () => dropdownMenu.classList.remove('show'));
      }

      if (signOutBtn) {
        signOutBtn.addEventListener('click', async (e) => {
          e.preventDefault();
          await authService.signOut();
          showToast('Signed out', 'info');
          window.location.reload();
        });
      }
    } else {
      navActions.innerHTML = `
        <button class="btn btn-secondary btn-sm" id="open-signin-btn">Sign In</button>
        <button class="btn btn-primary btn-sm" id="open-register-btn">Get Started</button>
      `;

      const openSignIn = document.getElementById('open-signin-btn');
      const openRegister = document.getElementById('open-register-btn');

      if (openSignIn) {
        openSignIn.addEventListener('click', () => {
          authModal.classList.add('active');
          if (tabLogin) tabLogin.click();
        });
      }

      if (openRegister) {
        openRegister.addEventListener('click', () => {
          authModal.classList.add('active');
          if (tabRegister) tabRegister.click();
        });
      }
    }
  });
}
