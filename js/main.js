/**
 * Book/Tow Desktop Spreadsheet Website JavaScript
 * Handles video play policy fallbacks, lightbox preview, and interaction enhancements
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Video Autoplay Fallback Handler
    const videos = document.querySelectorAll('.video-wrapper video');

    videos.forEach(video => {
        const wrapper = video.parentElement;
        const overlay = wrapper ? wrapper.querySelector('.video-play-overlay') : null;

        // Function to attempt playback
        const attemptPlay = () => {
            const playPromise = video.play();
            if (playPromise !== undefined) {
                playPromise.then(() => {
                    if (overlay) overlay.classList.remove('visible');
                }).catch(() => {
                    // Autoplay was blocked by browser
                    if (overlay) overlay.classList.add('visible');
                });
            }
        };

        // Try initial autoplay
        attemptPlay();

        // If overlay button exists, add click listener
        if (overlay) {
            overlay.addEventListener('click', () => {
                video.muted = false; // Unmute on explicit user interaction if desired or keep playing
                video.play().then(() => {
                    overlay.classList.remove('visible');
                }).catch(err => {
                    console.error('Video play error:', err);
                });
            });
        }

        // Clicking video directly toggles play/pause
        video.addEventListener('click', () => {
            if (video.paused) {
                video.play();
                if (overlay) overlay.classList.remove('visible');
            } else {
                video.pause();
                if (overlay) overlay.classList.add('visible');
            }
        });
    });

    // 2. Lightbox Gallery Preview
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxClose = document.querySelector('.lightbox-close');
    const galleryImages = document.querySelectorAll('.gallery-img');

    if (lightbox && lightboxImg) {
        galleryImages.forEach(img => {
            img.addEventListener('click', () => {
                lightboxImg.src = img.src;
                lightboxImg.alt = img.alt;
                lightbox.classList.add('active');
                lightbox.setAttribute('aria-hidden', 'false');
                document.body.style.overflow = 'hidden';
            });
        });

        const closeLightbox = () => {
            lightbox.classList.remove('active');
            lightbox.setAttribute('aria-hidden', 'true');
            document.body.style.overflow = '';
        };

        if (lightboxClose) {
            lightboxClose.addEventListener('click', closeLightbox);
        }

        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox || e.target === lightboxClose) {
                closeLightbox();
            }
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && lightbox.classList.contains('active')) {
                closeLightbox();
            }
        });
    }
});
