/**
 * Book/Tow Official Website Script
 * Handles:
 *  1. Context menu right-click suppression (Section 8)
 *  2. Screenshot Lightbox modal
 *  3. Video Autoplay & error handling
 *  4. Footer documentation & support info modal
 */

document.addEventListener('DOMContentLoaded', () => {

  /* ==========================================================================
     1. Disable Right-Click Context Menu (Section 8)
     ========================================================================== */
  document.addEventListener('contextmenu', (e) => {
    e.preventDefault();
    return false;
  });

  /* ==========================================================================
     2. Lightbox Screenshot Viewer Modal
     ========================================================================== */
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightbox-img');
  const lightboxCaption = document.getElementById('lightbox-caption');
  const lightboxCloseBtn = document.querySelector('.lightbox-close');
  const lightboxOverlay = document.querySelector('.lightbox-overlay');

  const galleryImages = document.querySelectorAll('.gallery-img');

  galleryImages.forEach((img) => {
    // Parent wrapper click listener
    const wrapper = img.closest('.image-wrapper');
    if (wrapper) {
      wrapper.addEventListener('click', () => {
        openLightbox(img.src, img.alt, img.dataset.title || img.alt);
      });
    }
  });

  function openLightbox(src, alt, caption) {
    if (!lightbox || !lightboxImg) return;
    lightboxImg.src = src;
    lightboxImg.alt = alt;
    if (lightboxCaption) {
      lightboxCaption.textContent = caption;
    }
    lightbox.classList.add('active');
    lightbox.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
  }

  function closeLightbox() {
    if (!lightbox) return;
    lightbox.classList.remove('active');
    lightbox.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  if (lightboxCloseBtn) lightboxCloseBtn.addEventListener('click', closeLightbox);
  if (lightboxOverlay) lightboxOverlay.addEventListener('click', closeLightbox);

  // Close on Escape key press
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeLightbox();
      closeInfoModal();
    }
  });

  /* ==========================================================================
     3. Video Autoplay & Graceful Fallback Handling
     ========================================================================== */
  const videos = document.querySelectorAll('.product-video');

  videos.forEach((video) => {
    // Ensure video properties for strict browser autoplay policy compliance
    video.muted = true;
    video.loop = true;
    video.playsInline = true;

    // Attempt play
    const playPromise = video.play();
    if (playPromise !== undefined) {
      playPromise.catch((error) => {
        console.warn('Autoplay prevented or video play failed:', error);
      });
    }

    // Handle missing or broken video sources gracefully
    video.addEventListener('error', () => {
      console.error('Error loading video source:', video.currentSrc);
      const parentContainer = video.closest('.video-player-container');
      if (parentContainer) {
        parentContainer.innerHTML = `
          <div class="video-fallback" style="padding: 60px 20px; text-align: center; color: #FFFFFF;">
            <h3>Product Video Demonstration</h3>
            <p style="margin-top: 10px; color: #94A3B8;">Video playback preview unavailable in this environment.</p>
          </div>
        `;
      }
    });
  });

  /* ==========================================================================
     4. Footer Info Modal
     ========================================================================== */
  const infoModal = document.getElementById('info-modal');
  const infoModalTitle = document.getElementById('info-modal-title');
  const infoModalBody = document.getElementById('info-modal-body');
  const infoModalClose = document.querySelector('.info-modal-close');
  const infoModalBackdrop = document.querySelector('.info-modal-backdrop');
  const footerModalTriggers = document.querySelectorAll('.footer-modal-trigger');

  const modalContents = {
    docs: {
      title: 'Book/Tow Documentation & User Guide',
      body: '<p>Complete documentation for Book/Tow v1.1.0 is bundled directly inside the downloadable package (<code>Booktow.zip</code>).</p><p style="margin-top: 10px;">Refer to the enclosed <code>README.md</code> for formula AST reference, keyboard shortcuts, and file format specifications.</p>'
    },
    support: {
      title: 'Book/Tow User Support',
      body: '<p>Book/Tow is an open-source portable spreadsheet application.</p><p style="margin-top: 10px;">For issues or feature requests, please inspect the included documentation package or consult the release repository.</p>'
    },
    privacy: {
      title: 'Privacy & Security Policy',
      body: '<p>Book/Tow is strictly a local offline application.</p><p style="margin-top: 10px;">We respect your privacy: <strong>Zero telemetry, zero tracking, and zero remote data collection</strong>. All formula processing and cell calculations remain completely on your local device.</p>'
    }
  };

  footerModalTriggers.forEach((trigger) => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      const modalKey = trigger.dataset.modal;
      if (modalContents[modalKey]) {
        openInfoModal(modalContents[modalKey].title, modalContents[modalKey].body);
      }
    });
  });

  function openInfoModal(title, bodyHtml) {
    if (!infoModal) return;
    if (infoModalTitle) infoModalTitle.textContent = title;
    if (infoModalBody) infoModalBody.innerHTML = bodyHtml;
    infoModal.classList.add('active');
    infoModal.setAttribute('aria-hidden', 'false');
  }

  function closeInfoModal() {
    if (!infoModal) return;
    infoModal.classList.remove('active');
    infoModal.setAttribute('aria-hidden', 'true');
  }

  if (infoModalClose) infoModalClose.addEventListener('click', closeInfoModal);
  if (infoModalBackdrop) infoModalBackdrop.addEventListener('click', closeInfoModal);

});
