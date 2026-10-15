import { getCurrentUser } from '../services/auth-service.js';
import { submitDesignPackage } from '../services/upload-service.js';
import { validateSubmission } from '../utils/validation.js';
import { showNotification } from '../utils/dom.js';

export async function renderUploadPage(container) {
  const user = getCurrentUser();

  if (!user) {
    container.innerHTML = `
      <div class="container py-12 text-center" style="max-width:540px;">
        <i class="fa-solid fa-lock" style="font-size:3rem; color:var(--color-primary); margin-bottom:1rem;"></i>
        <h2 style="font-size:1.75rem; font-weight:800; margin-bottom:0.5rem;">Authentication Required</h2>
        <p class="text-muted" style="margin-bottom:1.5rem;">You must sign in before uploading your login screen designs to the community platform.</p>
        <a href="/sign-in" data-link class="btn btn-primary btn-lg">Sign In to Continue</a>
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <div class="container py-8" style="max-width: 800px;">
      <div style="margin-bottom: 2rem;">
        <h1 style="font-size: 2.25rem; font-weight: 800; color: var(--color-secondary);">Upload Login Design</h1>
        <p class="text-muted">Share your login UI concept or template with creators worldwide.</p>
      </div>

      <form id="upload-form" class="auth-card" style="max-width:100%; margin:0;">
        <div class="form-group">
          <label class="form-label">Design Title *</label>
          <input type="text" name="title" class="form-input" placeholder="e.g., VisionOS Glassmorphism Login" required>
        </div>

        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1.25rem;">
          <div class="form-group">
            <label class="form-label">Category *</label>
            <select name="category" class="form-select" required>
              <option value="">Select Category</option>
              <option value="Glassmorphism">Glassmorphism</option>
              <option value="Cyberpunk">Cyberpunk</option>
              <option value="Minimal">Minimal</option>
              <option value="Illustration">Illustration</option>
              <option value="Dark Theme">Dark Theme</option>
              <option value="Neumorphism">Neumorphism</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Tags (comma separated)</label>
            <input type="text" name="tags" class="form-input" placeholder="glass, dark, visionos, animation">
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Description *</label>
          <textarea name="description" class="form-textarea" placeholder="Describe the design features, color scheme, interactive elements, and fonts..." required></textarea>
        </div>

        <div class="form-group">
          <label class="form-label">Preview Image Screenshot *</label>
          <div class="file-dropzone">
            <input type="file" id="preview-image-file" accept="image/*" required>
            <i class="fa-solid fa-cloud-arrow-up dropzone-icon"></i>
            <p style="font-weight:600; font-size:0.95rem;">Drag & drop image preview screenshot or <span style="color:var(--color-primary);">browse</span></p>
            <p class="text-muted" style="font-size:0.8rem; margin-top:0.25rem;">Supports JPG, PNG, WebP (Max 5MB)</p>
            <div id="image-filename" style="margin-top:0.5rem; font-weight:700; color:var(--color-primary);"></div>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Downloadable Package (.ZIP or HTML file) *</label>
          <div class="file-dropzone">
            <input type="file" id="zip-package-file" accept=".zip,.html" required>
            <i class="fa-solid fa-file-zipper dropzone-icon"></i>
            <p style="font-weight:600; font-size:0.95rem;">Upload template file or ZIP package</p>
            <p class="text-muted" style="font-size:0.8rem; margin-top:0.25rem;">Contains HTML, CSS, JS and asset resources (Max 25MB)</p>
            <div id="zip-filename" style="margin-top:0.5rem; font-weight:700; color:var(--color-primary);"></div>
          </div>
        </div>

        <button type="submit" id="btn-submit-upload" class="btn btn-primary btn-lg" style="width:100%; margin-top:1rem;">
          <i class="fa-solid fa-paper-plane"></i> Submit Design for Moderation Review
        </button>
      </form>
    </div>
  `;

  const form = container.querySelector('#upload-form');
  const previewInput = container.querySelector('#preview-image-file');
  const zipInput = container.querySelector('#zip-package-file');
  const imgNameDisplay = container.querySelector('#image-filename');
  const zipNameDisplay = container.querySelector('#zip-filename');

  previewInput.addEventListener('change', (e) => {
    if (e.target.files[0]) imgNameDisplay.textContent = e.target.files[0].name;
  });

  zipInput.addEventListener('change', (e) => {
    if (e.target.files[0]) zipNameDisplay.textContent = e.target.files[0].name;
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = {
      title: form.title.value.trim(),
      category: form.category.value,
      description: form.description.value.trim(),
      tags: form.tags.value.split(',').map(t => t.trim()).filter(Boolean),
      previewImageFile: previewInput.files[0],
      zipPackageFile: zipInput.files[0]
    };

    const validation = validateSubmission(formData);
    if (!validation.isValid) {
      const firstError = Object.values(validation.errors)[0];
      showNotification(firstError, 'danger');
      return;
    }

    const submitBtn = container.querySelector('#btn-submit-upload');
    submitBtn.disabled = true;
    submitBtn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i> Uploading Package...`;

    try {
      await submitDesignPackage(formData, user);
      showNotification('Design submitted successfully! Pending admin approval.', 'success');
      setTimeout(() => {
        window.location.href = '/my-uploads';
      }, 1000);
    } catch (err) {
      showNotification(err.message, 'danger');
      submitBtn.disabled = false;
      submitBtn.innerHTML = `<i class="fa-solid fa-paper-plane"></i> Submit Design for Moderation Review`;
    }
  });
}
