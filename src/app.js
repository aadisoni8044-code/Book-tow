import { renderNavbar } from './components/navbar.js';
import { renderFooter } from './components/footer.js';
import { initAuthListener } from './services/auth-service.js';

// Import Pages
import { renderHomePage } from './pages/home.js';
import { renderExplorePage } from './pages/explore.js';
import { renderDesignDetailsPage } from './pages/design-details.js';
import { renderPreviewPage } from './pages/preview.js';
import { renderUploadPage } from './pages/upload.js';
import { renderCreatorPage } from './pages/creator.js';
import { renderSignInPage } from './pages/sign-in.js';
import { renderDashboardPage } from './pages/dashboard.js';
import { renderMyUploadsPage } from './pages/my-uploads.js';
import { renderAdminPage } from './pages/admin.js';
import { renderReviewSubmissionsPage } from './pages/review-submissions.js';
import { renderNotFoundPage } from './pages/not-found.js';

const routes = {
  '/': renderHomePage,
  '/explore': renderExplorePage,
  '/design': renderDesignDetailsPage,
  '/preview': renderPreviewPage,
  '/upload': renderUploadPage,
  '/creator': renderCreatorPage,
  '/sign-in': renderSignInPage,
  '/dashboard': renderDashboardPage,
  '/my-uploads': renderMyUploadsPage,
  '/admin': renderAdminPage,
  '/review-submissions': renderReviewSubmissionsPage,
  '/404': renderNotFoundPage
};

export function navigateTo(path, params = {}) {
  const url = new URL(window.location.origin + path);
  Object.keys(params).forEach(key => url.searchParams.set(key, params[key]));
  window.history.pushState(params, '', url.pathname + url.search);
  handleRoute();
}

async function handleRoute() {
  const path = window.location.pathname;
  const mainContent = document.getElementById('main-content');
  const searchParams = new URLSearchParams(window.location.search);

  // Refresh Header Navigation
  renderNavbar();
  renderFooter();

  // Route matching
  let routeHandler = routes[path];
  if (!routeHandler) {
    routeHandler = renderNotFoundPage;
  }

  window.scrollTo(0, 0);
  try {
    await routeHandler(mainContent, searchParams);
  } catch (err) {
    console.error('Route rendering error:', err);
    mainContent.innerHTML = `<div class="container py-12"><div class="error-banner">An error occurred loading this view: ${err.message}</div></div>`;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  // Global click interception for client-side navigation
  document.addEventListener('click', (e) => {
    const link = e.target.closest('a[data-link]');
    if (link) {
      e.preventDefault();
      const href = link.getAttribute('href');
      if (href) {
        navigateTo(href);
      }
    }
  });

  window.addEventListener('popstate', handleRoute);

  // Initialize Auth state listener
  initAuthListener(() => {
    renderNavbar();
    handleRoute();
  });
});
