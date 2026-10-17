/**
 * Project A — Dark Brutalist Software Download Website
 * Interactive behaviors, dynamic metadata, asset error handling & fallbacks
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Dynamic Copyright Year
    const yearElem = document.getElementById('current-year');
    if (yearElem) {
        yearElem.textContent = new Date().getFullYear();
    }

    // 2. Download Button File Existence Check
    const downloadBtn = document.getElementById('download-button');
    const downloadStatus = document.getElementById('download-status');

    if (downloadBtn && downloadStatus) {
        // Pre-check if a.zip exists
        fetch('./a.zip', { method: 'HEAD' })
            .then(response => {
                if (!response.ok) {
                    showDownloadUnavailable();
                }
            })
            .catch(() => {
                showDownloadUnavailable();
            });

        downloadBtn.addEventListener('click', (e) => {
            fetch('./a.zip', { method: 'HEAD' })
                .then(response => {
                    if (!response.ok) {
                        e.preventDefault();
                        showDownloadUnavailable();
                    }
                })
                .catch(() => {
                    e.preventDefault();
                    showDownloadUnavailable();
                });
        });
    }

    function showDownloadUnavailable() {
        if (downloadStatus) {
            downloadStatus.textContent = "The download file (a.zip) is not yet available in the directory.";
            downloadStatus.style.display = 'block';
        }
    }

    // 3. Image Loading & Fallback Error Handler
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('error', function() {
            handleMissingImage(this);
        });

        // Trigger check if already broken or empty
        if (img.complete && img.naturalWidth === 0 && img.src) {
            handleMissingImage(img);
        }
    });

    function handleMissingImage(imgElement) {
        const altText = imgElement.alt || 'Image Asset';
        const srcAttr = imgElement.getAttribute('src') || './a.png';
        const parent = imgElement.parentElement;

        const placeholder = document.createElement('div');
        placeholder.className = 'media-placeholder';
        placeholder.innerHTML = `
            <span class="media-placeholder-title">[ MEDIA MISSING ]</span>
            <span>${escapeHTML(altText)} (${escapeHTML(srcAttr)})</span>
        `;

        if (parent && parent.classList.contains('logo-wrapper')) {
            parent.replaceChild(placeholder, imgElement);
        } else if (parent && parent.classList.contains('image-wrapper')) {
            parent.replaceChild(placeholder, imgElement);
        } else if (parent) {
            imgElement.style.display = 'none';
            parent.appendChild(placeholder);
        }
    }

    // 4. Video Fallback Handler
    const video = document.getElementById('demo-video');
    if (video) {
        video.addEventListener('error', () => {
            handleMissingVideo(video);
        }, true);

        // Check if video source fails or is empty
        const source = video.querySelector('source');
        if (source) {
            source.addEventListener('error', () => {
                handleMissingVideo(video);
            });
        }
    }

    function handleMissingVideo(videoElement) {
        const container = videoElement.parentElement;
        if (!container) return;

        const placeholder = document.createElement('div');
        placeholder.className = 'media-placeholder';
        placeholder.style.position = 'absolute';
        placeholder.style.top = '0';
        placeholder.style.left = '0';
        placeholder.style.width = '100%';
        placeholder.style.height = '100%';
        placeholder.innerHTML = `
            <span class="media-placeholder-title">[ VIDEO UNAVAILABLE ]</span>
            <span>Product demonstration video (./a.mp4) is not available.</span>
        `;

        videoElement.style.display = 'none';
        container.appendChild(placeholder);
    }

    // 5. Utility function to escape HTML
    function escapeHTML(str) {
        return str.replace(/[&<>'"]/g,
            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag] || tag)
        );
    }
});
