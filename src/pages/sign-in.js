import { signInWithEmail, signUpWithEmail, signInWithGoogle } from '../services/auth-service.js';
import { showNotification } from '../utils/dom.js';

export async function renderSignInPage(container) {
  let isSignUpMode = false;

  const renderForm = () => {
    container.innerHTML = `
      <div class="container py-8">
        <div class="auth-card">
          <h1 class="auth-title">${isSignUpMode ? 'Create Creator Account' : 'Welcome Back'}</h1>
          <p class="auth-subtitle">${isSignUpMode ? 'Join our marketplace of login UI designers' : 'Sign in to manage and submit your designs'}</p>

          <button id="btn-google-auth" class="btn btn-outline" style="width:100%; margin-bottom: 1rem;">
            <i class="fa-brands fa-google text-rose-500"></i> Continue with Google
          </button>

          <div class="auth-divider">or email</div>

          <form id="auth-form">
            ${isSignUpMode ? `
              <div class="form-group">
                <label class="form-label">Display Name *</label>
                <input type="text" name="displayName" class="form-input" placeholder="Alex Rivera" required>
              </div>
            ` : ''}

            <div class="form-group">
              <label class="form-label">Email Address *</label>
              <input type="email" name="email" class="form-input" placeholder="creator@loginscreen.io" required>
            </div>

            <div class="form-group">
              <label class="form-label">Password *</label>
              <input type="password" name="password" class="form-input" placeholder="••••••••" required minlength="6">
            </div>

            <button type="submit" id="btn-submit-auth" class="btn btn-primary btn-lg" style="width:100%; margin-top:0.5rem;">
              ${isSignUpMode ? 'Create Account' : 'Sign In'}
            </button>
          </form>

          <p class="text-center text-muted" style="font-size:0.875rem; margin-top:1.5rem;">
            ${isSignUpMode ? 'Already have an account?' : "Don't have an account?"}
            <button id="btn-toggle-mode" style="color:var(--color-primary); font-weight:700; text-decoration:underline;">
              ${isSignUpMode ? 'Sign In' : 'Sign Up'}
            </button>
          </p>
        </div>
      </div>
    `;

    const form = container.querySelector('#auth-form');
    const googleBtn = container.querySelector('#btn-google-auth');
    const toggleBtn = container.querySelector('#btn-toggle-mode');

    toggleBtn.addEventListener('click', () => {
      isSignUpMode = !isSignUpMode;
      renderForm();
    });

    googleBtn.addEventListener('click', async () => {
      try {
        await signInWithGoogle();
        showNotification('Signed in with Google!', 'success');
        window.location.href = '/dashboard';
      } catch (err) {
        showNotification(err.message, 'danger');
      }
    });

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = form.email.value.trim();
      const password = form.password.value;

      try {
        if (isSignUpMode) {
          const name = form.displayName.value.trim();
          await signUpWithEmail(email, password, name);
          showNotification('Account created successfully!', 'success');
        } else {
          await signInWithEmail(email, password);
          showNotification('Welcome back!', 'success');
        }
        window.location.href = '/dashboard';
      } catch (err) {
        showNotification(err.message, 'danger');
      }
    });
  };

  renderForm();
}
