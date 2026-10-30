/* ==========================================================================
   Project A - Dark Brutalist Software Download Website JavaScript
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Dynamic Current Year in Footer
  const yearSpan = document.getElementById('current-year');
  if (yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
  }

  // 2. Download Button Handler & Availability Checking
  const downloadBtn = document.getElementById('download-btn');
  const downloadStatus = document.getElementById('download-status');

  if (downloadBtn && downloadStatus) {
    downloadBtn.addEventListener('click', (e) => {
      fetch('./a.zip', { method: 'HEAD' })
        .then((response) => {
          if (!response.ok) {
            e.preventDefault();
            downloadStatus.className = 'download-status error';
            downloadStatus.textContent = 'Notice: Download file (a.zip) is not yet available in the directory.';
          } else {
            downloadStatus.className = 'download-status info';
            downloadStatus.textContent = 'Starting download for a.zip...';
            setTimeout(() => {
              downloadStatus.style.display = 'none';
            }, 5000);
          }
        })
        .catch(() => {
          // If HEAD fails due to CORS or local origin, allow standard browser download behavior
        });
    });
  }

  // 3. Two Video Error Handling & Fallbacks
  setupVideoFallback('demo-video-1', 'video-fallback-1');
  setupVideoFallback('demo-video-2', 'video-fallback-2');

  function setupVideoFallback(videoId, fallbackId) {
    const video = document.getElementById(videoId);
    const fallback = document.getElementById(fallbackId);

    if (video && fallback) {
      video.addEventListener('error', () => {
        video.style.display = 'none';
        fallback.classList.remove('hidden');
      });

      video.play().catch((err) => {
        // Playback deferred by autoplay policy - browser native play button remains available
      });
    }
  }

  // 4. Lightbox Gallery Modal
  const modal = document.getElementById('lightbox-modal');
  const modalImg = document.getElementById('lightbox-img');
  const modalCaption = document.getElementById('lightbox-caption');
  const modalClose = document.getElementById('lightbox-close');
  const modalOverlay = document.getElementById('lightbox-overlay');
  const clickableCards = document.querySelectorAll('.clickable-gallery-card');

  clickableCards.forEach((card) => {
    card.addEventListener('click', () => {
      const fullSrc = card.getAttribute('data-fullsrc');
      const title = card.getAttribute('data-title');

      if (modal && modalImg && fullSrc) {
        modalImg.src = fullSrc;
        modalImg.alt = title || 'Enlarged Screenshot';
        if (modalCaption) modalCaption.textContent = title || '';
        modal.classList.add('active');
        modal.setAttribute('aria-hidden', 'false');
      }
    });
  });

  function closeModal() {
    if (modal) {
      modal.classList.remove('active');
      modal.setAttribute('aria-hidden', 'true');
    }
  }

  if (modalClose) modalClose.addEventListener('click', closeModal);
  if (modalOverlay) modalOverlay.addEventListener('click', closeModal);

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal && modal.classList.contains('active')) {
      closeModal();
    }
  });

  // 5. Back To Top Smooth Scroll
  const backToTopBtn = document.getElementById('back-to-top');
  if (backToTopBtn) {
    backToTopBtn.addEventListener('click', (e) => {
      e.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  // 6. Lightweight Background Canvas Arcade Game
  initBgCanvasGame();
});

function initBgCanvasGame() {
  const canvas = document.getElementById('bg-game-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  // Check reduced motion preference
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReducedMotion) {
    canvas.style.display = 'none';
    return;
  }

  let width, height;
  let animFrameId = null;
  let isTabVisible = true;

  // Responsive particle density
  const isMobile = window.innerWidth <= 768;
  const particleCount = isMobile ? 12 : 30;
  const particles = [];
  const collectibles = [];

  function resizeCanvas() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  }

  window.addEventListener('resize', resizeCanvas);
  resizeCanvas();

  // Create subtle dark brutalist shape particles
  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      size: Math.random() * 8 + 4,
      vx: (Math.random() - 0.5) * 0.6,
      vy: (Math.random() - 0.5) * 0.6,
      type: Math.floor(Math.random() * 3), // 0: square, 1: triangle, 2: dot
      rotation: Math.random() * Math.PI * 2,
      vRot: (Math.random() - 0.5) * 0.02,
      opacity: Math.random() * 0.25 + 0.1
    });
  }

  // Collectible glow dots
  const collectibleCount = isMobile ? 5 : 12;
  for (let i = 0; i < collectibleCount; i++) {
    collectibles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      radius: Math.random() * 3 + 2,
      pulse: Math.random() * Math.PI,
      pulseSpeed: 0.03 + Math.random() * 0.02
    });
  }

  function renderGame() {
    if (!isTabVisible) return;

    ctx.clearRect(0, 0, width, height);

    // Draw ambient grid accent nodes
    for (let i = 0; i < collectibles.length; i++) {
      const c = collectibles[i];
      c.pulse += c.pulseSpeed;
      const alpha = 0.15 + Math.sin(c.pulse) * 0.1;

      ctx.fillStyle = `rgba(139, 92, 246, ${alpha})`;
      ctx.beginPath();
      ctx.arc(c.x, c.y, c.radius + Math.sin(c.pulse) * 1.5, 0, Math.PI * 2);
      ctx.fill();
    }

    // Draw moving geometric shapes
    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];

      p.x += p.vx;
      p.y += p.vy;
      p.rotation += p.vRot;

      // Wrap boundaries
      if (p.x < -20) p.x = width + 20;
      if (p.x > width + 20) p.x = -20;
      if (p.y < -20) p.y = height + 20;
      if (p.y > height + 20) p.y = -20;

      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate(p.rotation);
      ctx.fillStyle = `rgba(139, 92, 246, ${p.opacity})`;
      ctx.strokeStyle = `rgba(255, 255, 255, ${p.opacity * 0.8})`;
      ctx.lineWidth = 1;

      if (p.type === 0) {
        // Square shape
        ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
        ctx.strokeRect(-p.size / 2, -p.size / 2, p.size, p.size);
      } else if (p.type === 1) {
        // Triangle shape
        ctx.beginPath();
        ctx.moveTo(0, -p.size);
        ctx.lineTo(p.size, p.size);
        ctx.lineTo(-p.size, p.size);
        ctx.closePath();
        ctx.stroke();
      } else {
        // Circle dot shape
        ctx.beginPath();
        ctx.arc(0, 0, p.size / 2, 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.restore();
    }

    animFrameId = requestAnimationFrame(renderGame);
  }

  // Handle visibility change to conserve CPU resources
  document.addEventListener('visibilitychange', () => {
    isTabVisible = !document.hidden;
    if (isTabVisible) {
      animFrameId = requestAnimationFrame(renderGame);
    } else if (animFrameId) {
      cancelAnimationFrame(animFrameId);
    }
  });

  animFrameId = requestAnimationFrame(renderGame);
}
