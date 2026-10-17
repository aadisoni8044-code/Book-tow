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
      // Check if file exists via HEAD request
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
          // If HEAD request fails due to local file protocol or server restriction, let native link download attempt proceed
        });
    });
  }

  // 3. Video Error Handling & Fallback Display
  const video = document.getElementById('demo-video');
  const videoFallback = document.getElementById('video-fallback');

  if (video && videoFallback) {
    video.addEventListener('error', () => {
      video.style.display = 'none';
      videoFallback.classList.remove('hidden');
    });

    // Handle autoplay restrictions gracefully
    video.play().catch((err) => {
      console.log('Autoplay deferred by browser policy:', err);
    });
  }

  // 4. Smooth Back To Top Navigation
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
});
