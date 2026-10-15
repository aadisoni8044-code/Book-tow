export function createSearchBar(onSearchChange) {
  const wrapper = document.createElement('div');
  wrapper.className = 'search-field';

  wrapper.innerHTML = `
    <i class="fa-solid fa-magnifying-glass"></i>
    <input type="text" placeholder="Search login designs, categories, or tags..." aria-label="Search designs">
  `;

  const input = wrapper.querySelector('input');
  let debounceTimeout;

  input.addEventListener('input', (e) => {
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(() => {
      onSearchChange(e.target.value.trim());
    }, 300);
  });

  return wrapper;
}
