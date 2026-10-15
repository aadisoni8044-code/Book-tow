import { getPublishedDesigns } from '../services/design-service.js';
import { renderDesignGrid } from '../components/design-grid.js';
import { createSearchBar } from '../components/search-bar.js';
import { createCategoryFilter } from '../components/category-filter.js';

export async function renderHomePage(container) {
  container.innerHTML = `
    <section style="background: linear-gradient(180deg, #EEF2FF 0%, #F8FAFC 100%); padding: 5rem 0 3.5rem; text-align: center;">
      <div class="container" style="max-width: 860px;">
        <span class="badge badge-primary mb-4" style="font-size: 0.85rem; padding: 0.35rem 0.85rem;">
          <i class="fa-solid fa-sparkles"></i> High-Quality Login UI Marketplace
        </span>
        <h1 style="font-size: 3rem; font-weight: 800; color: var(--color-secondary); line-height: 1.15; margin-bottom: 1.25rem;">
          Discover & Share Modern Authentication Interfaces
        </h1>
        <p style="font-size: 1.15rem; color: var(--text-muted); margin-bottom: 2.25rem;">
          Explore a curated marketplace of glassmorphic, 3D animated, and cybernetic login screen templates crafted by top UI designers.
        </p>

        <div id="hero-search-mount" style="max-width: 600px; margin: 0 auto 1.5rem;"></div>
        <div id="hero-categories-mount" style="display: flex; justify-content: center; gap: 0.5rem;"></div>
      </div>
    </section>

    <section class="gallery-section container">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 1.5rem;">
        <div>
          <h2 style="font-size: 1.5rem; font-weight: 800;">Featured Designs</h2>
          <p class="text-muted" style="font-size:0.9rem;">Handpicked authentication layouts ready for download</p>
        </div>
        <a href="/explore" data-link class="btn btn-outline btn-sm">View All Gallery <i class="fa-solid fa-arrow-right"></i></a>
      </div>

      <div id="featured-grid-container"></div>
    </section>
  `;

  const searchMount = container.querySelector('#hero-search-mount');
  const categoriesMount = container.querySelector('#hero-categories-mount');
  const gridContainer = container.querySelector('#featured-grid-container');

  searchMount.appendChild(createSearchBar((searchTerm) => {
    window.location.href = `/explore?search=${encodeURIComponent(searchTerm)}`;
  }));

  categoriesMount.appendChild(createCategoryFilter('All', (category) => {
    window.location.href = `/explore?category=${encodeURIComponent(category)}`;
  }));

  // Initial loading state
  renderDesignGrid(gridContainer, [], true);

  const designs = await getPublishedDesigns();
  renderDesignGrid(gridContainer, designs.slice(0, 8), false);
}
