const CATEGORIES = ['All', 'Glassmorphism', 'Cyberpunk', 'Minimal', 'Illustration', 'Dark Theme', 'Neumorphism'];

export function createCategoryFilter(activeCategory, onCategoryChange) {
  const container = document.createElement('div');
  container.className = 'category-pills';

  CATEGORIES.forEach(cat => {
    const btn = document.createElement('button');
    btn.className = `pill-btn ${cat.toLowerCase() === (activeCategory || 'All').toLowerCase() ? 'active' : ''}`;
    btn.textContent = cat;

    btn.addEventListener('click', () => {
      container.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      onCategoryChange(cat);
    });

    container.appendChild(btn);
  });

  return container;
}
