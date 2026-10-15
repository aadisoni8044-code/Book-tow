export function createModal({ title, content, confirmText = 'Confirm', onConfirm, onCancel }) {
  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay';

  overlay.innerHTML = `
    <div class="modal-card">
      <div class="modal-header">
        <h3 style="font-weight:700; font-size:1.1rem;">${title}</h3>
        <button class="btn-close" style="font-size:1.25rem; color:var(--text-muted);">&times;</button>
      </div>
      <div class="modal-body">
        ${typeof content === 'string' ? `<p>${content}</p>` : ''}
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary btn-sm btn-cancel">Cancel</button>
        <button class="btn btn-primary btn-sm btn-confirm">${confirmText}</button>
      </div>
    </div>
  `;

  if (typeof content !== 'string' && content instanceof HTMLElement) {
    overlay.querySelector('.modal-body').appendChild(content);
  }

  const closeBtn = overlay.querySelector('.btn-close');
  const cancelBtn = overlay.querySelector('.btn-cancel');
  const confirmBtn = overlay.querySelector('.btn-confirm');

  const destroy = () => overlay.remove();

  closeBtn.addEventListener('click', destroy);
  cancelBtn.addEventListener('click', () => {
    if (onCancel) onCancel();
    destroy();
  });

  confirmBtn.addEventListener('click', () => {
    if (onConfirm) onConfirm();
    destroy();
  });

  return { overlay, destroy };
}
