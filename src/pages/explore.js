import { getPublishedDesigns } from '../services/design-service.js';
import { renderDesignGrid } from '../components/design-grid.js';
import { createSearchBar } from '../components/search-bar.js';
import { createCategoryFilter } from '../components/category-filter.js';

export async function renderExplorePage(container, searchParams) {
  let activeCategory = searchParams.get('category') || 'All';
  let activeSearch = searchParams.get('search') || '';

  container.innerHTML = `
    <div class="container py-8">
      <div style="margin-bottom: 2rem;">
        <h1 style="font-size: 2.25rem; font-weight: 800; color: var(--color-secondary);">Explore Design Gallery</h1>
        <p class="text-muted">Browse top login UI concepts, glassmorphism templates, and interactive forms.</p>
      </div>

      <div class="gallery-header">
        <div class="search-filter-bar">
          <div id="explore-search-mount"></div>
        </div>
        <div id="explore-categories-mount"></div>
      </div>

      <div id="explore-grid-mount"></div>
    </div>
  `;

  const searchMount = container.querySelector('#explore-search-mount');
  const categoriesMount = container.querySelector('#explore-categories-mount');
  const gridMount = container.querySelector('#explore-grid-mount');

  const updateGallery = async () => {
    renderDesignGrid(gridMount, [], true);
    const designs = await getPublishedDesigns({
      category: activeCategory,
      search: activeSearch
    });
    renderDesignGrid(gridMount, designs, false);
  };

  searchMount.appendChild(createSearchBar((searchTerm) => {
    activeSearch = searchTerm;
    updateGallery();
  }));

  categoriesMount.appendChild(createCategoryFilter(activeCategory, (category) => {
    activeCategory = category;
    updateGallery();
  }));

  await updateGallery();
}
