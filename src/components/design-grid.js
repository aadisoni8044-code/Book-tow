import { createDesignCard } from './design-card.js';
import { createSkeletonGrid } from './loading-state.js';

export function renderDesignGrid(container, designs, isLoading = false) {
  if (!container) return;

  container.innerHTML = '';

  if (isLoading) {
    container.appendChild(createSkeletonGrid());
    return;
  }

  if (!designs || designs.length === 0) {
    container.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 4rem 1rem;" class="text-muted">
        <i class="fa-solid fa-folder-open" style="font-size: 3rem; margin-bottom: 1rem; color: var(--border-hover);"></i>
        <h3 style="font-size: 1.25rem; font-weight:700; color:var(--text-main);">No login screen designs found</h3>
        <p>Try adjusting your search criteria or explore other categories.</p>
      </div>
    `;
    return;
  }

  const grid = document.createElement('div');
  grid.className = 'design-grid';

  designs.forEach(design => {
    grid.appendChild(createDesignCard(design));
  });

  container.appendChild(grid);
}
