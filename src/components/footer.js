export function renderFooter() {
  const container = document.getElementById('footer-container');
  if (!container) return;

  container.innerHTML = `
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a href="/" data-link class="brand-logo" style="color:var(--text-white);">
            <svg viewBox="0 0 64 64" width="32" height="32">
              <rect width="64" height="64" rx="16" fill="#4F46E5"/>
              <rect x="18" y="14" width="28" height="36" rx="6" fill="#FFFFFF"/>
            </svg>
            <span>LoginScreen Community</span>
          </a>
          <p>The premier modern gallery and design marketplace for high-performance authentication UI, glassmorphic login screens, and developer templates.</p>
        </div>

        <div class="footer-column">
          <h4>Explore</h4>
          <ul class="footer-links">
            <li><a href="/explore?category=Glassmorphism" data-link>Glassmorphism</a></li>
            <li><a href="/explore?category=Cyberpunk" data-link>Cyberpunk</a></li>
            <li><a href="/explore?category=Minimal" data-link>Minimalist</a></li>
            <li><a href="/explore?category=Illustration" data-link>3D & Illustration</a></li>
          </ul>
        </div>

        <div class="footer-column">
          <h4>Community</h4>
          <ul class="footer-links">
            <li><a href="/upload" data-link>Upload Design</a></li>
            <li><a href="/explore" data-link>Featured Creators</a></li>
            <li><a href="/sign-in" data-link>Creator Portal</a></li>
          </ul>
        </div>

        <div class="footer-column">
          <h4>Platform</h4>
          <ul class="footer-links">
            <li><a href="https://github.com" target="_blank">Documentation</a></li>
            <li><a href="https://firebase.google.com" target="_blank">Firebase Services</a></li>
            <li><a href="https://netlify.com" target="_blank">Netlify Functions</a></li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <p>&copy; ${new Date().getFullYear()} LoginScreen Community Platform. Free & Open Creative Ecosystem.</p>
        <p>Built with ES Modules & Firebase Architecture</p>
      </div>
    </div>
  `;
}
