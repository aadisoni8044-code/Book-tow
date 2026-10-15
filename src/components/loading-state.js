export function createSkeletonGrid(count = 8) {
  const grid = document.createElement('div');
  grid.className = 'design-grid';

  for (let i = 0; i < count; i++) {
    const card = document.createElement('div');
    card.className = 'skeleton-card';
    card.innerHTML = `
      <div class="skeleton-box skeleton-media"></div>
      <div class="skeleton-box skeleton-title"></div>
      <div class="skeleton-box skeleton-text"></div>
    `;
    grid.appendChild(card);
  }

  return grid;
}
