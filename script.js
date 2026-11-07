/**
 * DESIGNING/TOW — Interactive Client Script
 * Handles video playback management, control overlays, and download feedback.
 */

document.addEventListener('DOMContentLoaded', () => {
  initVideos();
  initDownloadAnalytics();
});

/**
 * Initializes video controls and ensures autoplay on modern browsers.
 */
function initVideos() {
  const videos = [
    document.getElementById('video-player-a'),
    document.getElementById('video-player-b')
  ];

  videos.forEach((video) => {
    if (!video) return;

    // Guarantee browser policy compliance for autoplay
    video.muted = true;
    video.playsInline = true;

    const playPromise = video.play();
    if (playPromise !== undefined) {
      playPromise.catch(() => {
        // Autoplay policy prevented playback, keep paused until user interacts
      });
    }

    // Attach overlay control listeners
    const controlsContainer = document.querySelector(`.video-overlay-controls[data-video="${video.id}"]`);
    if (!controlsContainer) return;

    const pauseBtn = controlsContainer.querySelector('.pause-toggle');
    const soundBtn = controlsContainer.querySelector('.sound-toggle');

    if (pauseBtn) {
      pauseBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (video.paused) {
          video.play();
          pauseBtn.classList.remove('paused');
          pauseBtn.setAttribute('title', 'Pause Video');
        } else {
          video.pause();
          pauseBtn.classList.add('paused');
          pauseBtn.setAttribute('title', 'Play Video');
        }
      });

      // Update button state if video is paused/played through other events
      video.addEventListener('play', () => pauseBtn.classList.remove('paused'));
      video.addEventListener('pause', () => pauseBtn.classList.add('paused'));
    }

    if (soundBtn) {
      soundBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        video.muted = !video.muted;
        if (video.muted) {
          soundBtn.classList.remove('unmuted');
          soundBtn.setAttribute('title', 'Unmute Video');
        } else {
          soundBtn.classList.add('unmuted');
          soundBtn.setAttribute('title', 'Mute Video');
        }
      });
    }
  });

  // IntersectionObserver to pause off-screen videos and conserve system resources
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        const video = entry.target;
        if (entry.isIntersecting) {
          if (video.paused && !video.dataset.manualPause) {
            video.play().catch(() => {});
          }
        } else {
          if (!video.paused) {
            video.pause();
          }
        }
      });
    }, { threshold: 0.25 });

    videos.forEach((video) => {
      if (video) observer.observe(video);
    });
  }
}

/**
 * Handles smooth download interactions and visual feedback on the main CTA button.
 */
function initDownloadAnalytics() {
  const downloadBtn = document.getElementById('main-download-button');
  if (!downloadBtn) return;

  downloadBtn.addEventListener('click', () => {
    const originalText = downloadBtn.querySelector('.btn-heading');
    if (!originalText) return;

    const prevHeading = originalText.textContent;
    originalText.textContent = 'Downloading Installer...';

    setTimeout(() => {
      originalText.textContent = prevHeading;
    }, 4000);
  });
}
