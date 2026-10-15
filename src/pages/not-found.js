export async function renderNotFoundPage(container) {
  container.innerHTML = `
    <div class="container py-12 text-center" style="max-width: 600px;">
      <h1 style="font-size: 6rem; font-weight: 800; color: var(--color-primary); line-height: 1;">404</h1>
      <h2 style="font-size: 1.75rem; font-weight: 700; margin-bottom: 0.75rem;">Page Not Found</h2>
      <p class="text-muted" style="margin-bottom: 2rem;">
        The login screen design or route you requested could not be located.
      </p>
      <a href="/" data-link class="btn btn-primary btn-lg">Return to Gallery Home</a>
    </div>
  `;
}
