/**
 * DOM Manipulation Helpers
 */

export function createElement(tag, attributes = {}, children = []) {
  const element = document.createElement(tag);

  Object.entries(attributes).forEach(([key, value]) => {
    if (key === 'className') {
      element.className = value;
    } else if (key === 'dataset') {
      Object.entries(value).forEach(([dataKey, dataValue]) => {
        element.dataset[dataKey] = dataValue;
      });
    } else if (key.startsWith('on') && typeof value === 'function') {
      element.addEventListener(key.substring(2).toLowerCase(), value);
    } else {
      element.setAttribute(key, value);
    }
  });

  children.forEach(child => {
    if (typeof child === 'string') {
      element.appendChild(document.createTextNode(child));
    } else if (child instanceof HTMLElement) {
      element.appendChild(child);
    }
  });

  return element;
}

export function clearContainer(container) {
  if (typeof container === 'string') {
    container = document.querySelector(container);
  }
  if (container) {
    container.innerHTML = '';
  }
}

export function showNotification(message, type = 'info', duration = 3000) {
  const container = document.getElementById('notification-container');
  if (!container) return;

  const toast = createElement('div', { className: `toast toast-${type}` }, [
    createElement('i', { className: getToastIcon(type) }),
    createElement('span', {}, [message])
  ]);

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

function getToastIcon(type) {
  switch (type) {
    case 'success': return 'fa-solid fa-circle-check text-emerald-500';
    case 'danger': return 'fa-solid fa-circle-xmark text-rose-500';
    case 'warning': return 'fa-solid fa-triangle-exclamation text-amber-500';
    default: return 'fa-solid fa-circle-info text-indigo-500';
  }
}
