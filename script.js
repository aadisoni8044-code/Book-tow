/**
 * JPS script - Main JavaScript Interactions
 */

document.addEventListener('DOMContentLoaded', () => {
  /* --- Mobile Navigation Drawer Toggle --- */
  const mobileToggle = document.getElementById('mobileToggle');
  const navMenu = document.getElementById('navMenu');
  const navLinks = document.querySelectorAll('.nav-link');

  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', () => {
      const isOpen = navMenu.classList.contains('active');
      navMenu.classList.toggle('active');
      mobileToggle.classList.toggle('active');
      mobileToggle.setAttribute('aria-expanded', !isOpen);
    });

    // Close mobile menu when clicking a navigation link
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        if (navMenu.classList.contains('active')) {
          navMenu.classList.remove('active');
          mobileToggle.classList.remove('active');
          mobileToggle.setAttribute('aria-expanded', 'false');
        }
      });
    });
  }

  /* --- Navigation Highlight on Scroll --- */
  const sections = document.querySelectorAll('section[id]');

  const handleScrollActiveLink = () => {
    const scrollY = window.pageYOffset;

    sections.forEach(current => {
      const sectionHeight = current.offsetHeight;
      const sectionTop = current.offsetTop - 100;
      const sectionId = current.getAttribute('id');
      const targetLink = document.querySelector(`.nav-menu a[href*="${sectionId}"]`);

      if (targetLink) {
        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
          targetLink.classList.add('active');
        } else {
          targetLink.classList.remove('active');
        }
      }
    });
  };

  window.addEventListener('scroll', handleScrollActiveLink);

  /* --- Image Lightbox Modal Handler --- */
  const lightboxModal = document.getElementById('lightboxModal');
  const lightboxOverlay = document.getElementById('lightboxOverlay');
  const lightboxImage = document.getElementById('lightboxImage');
  const lightboxCaption = document.getElementById('lightboxCaption');
  const lightboxClose = document.getElementById('lightboxClose');
  const galleryCards = document.querySelectorAll('.gallery-card');

  const openLightbox = (imgSrc, captionText) => {
    if (!lightboxModal || !lightboxImage) return;
    lightboxImage.src = imgSrc;
    lightboxImage.alt = captionText || 'JPS script showcase';
    if (lightboxCaption) {
      lightboxCaption.textContent = captionText || '';
    }
    lightboxModal.classList.add('active');
    lightboxModal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  };

  const closeLightbox = () => {
    if (!lightboxModal) return;
    lightboxModal.classList.remove('active');
    lightboxModal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  };

  galleryCards.forEach(card => {
    card.addEventListener('click', () => {
      const imgSrc = card.getAttribute('data-lightbox') || card.querySelector('img')?.src;
      const captionText = card.querySelector('.gallery-caption h4')?.textContent;
      if (imgSrc) {
        openLightbox(imgSrc, captionText);
      }
    });
  });

  if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);
  if (lightboxOverlay) lightboxOverlay.addEventListener('click', closeLightbox);

  // Close lightbox on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && lightboxModal && lightboxModal.classList.contains('active')) {
      closeLightbox();
    }
  });

  /* --- Video Autoplay Fallback and Safety --- */
  const heroVideo = document.querySelector('.hero-video');
  if (heroVideo) {
    // Ensure hero video remains muted for reliable browser autoplay
    heroVideo.muted = true;
    heroVideo.play().catch(err => {
      console.log('Hero video autoplay blocked or pending interaction:', err);
    });
  }

  /* --- Download Button Click Feedback --- */
  const downloadButtons = document.querySelectorAll('a[download]');
  downloadButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      console.log('Jps.zip download initiated.');
    });
  });
});
