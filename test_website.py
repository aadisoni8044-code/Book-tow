import asyncio
import os
import subprocess
import time
from playwright.async_api import async_playwright

async def main():
    # Start server
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8080"])
    time.sleep(2)

    os.makedirs("test_results", exist_ok=True)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(viewport={'width': 1280, 'height': 800})
            page = await context.new_page()

            # Listen for console errors
            console_errors = []
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

            print("Navigating to http://localhost:8080/ ...")
            response = await page.goto("http://localhost:8080/")
            assert response.status == 200, "Failed to load index.html"

            # 1. Verify Logo & Header
            logo = page.locator("#main-logo")
            assert await logo.is_visible(), "Hero logo not visible"
            print("Logo verified.")

            # 2. Verify Download Section
            download_btn = page.locator("#download-now-btn")
            assert await download_btn.is_visible(), "Download Now button not visible"
            href = await download_btn.get_attribute("href")
            assert href == "downloads/Booktow.zip", f"Incorrect download link: {href}"
            print("Download section verified.")

            # 3. Verify Videos
            video_a = page.locator("#video-a")
            video_b = page.locator("#video-b")
            assert await video_a.is_visible(), "Video A not visible"
            assert await video_b.is_visible(), "Video B not visible"
            print("Videos verified.")

            # 4. Verify Gallery Images
            gallery_imgs = page.locator(".gallery-img")
            count = await gallery_imgs.count()
            assert count == 4, f"Expected 4 gallery images, found {count}"

            # Check image order: b.png, c.png, d.png, e.png
            expected_srcs = ["assets/b.png", "assets/c.png", "assets/d.png", "assets/e.png"]
            for i in range(4):
                src = await gallery_imgs.nth(i).get_attribute("src")
                assert src == expected_srcs[i], f"Image index {i} mismatch: got {src}, expected {expected_srcs[i]}"
            print("Gallery screenshot order verified (b.png -> c.png -> d.png -> e.png).")

            # 5. Verify Lightbox interaction
            first_img_wrapper = page.locator(".image-wrapper").first
            await first_img_wrapper.click()
            await page.wait_for_timeout(500)

            lightbox = page.locator("#lightbox")
            assert "active" in (await lightbox.get_attribute("class")), "Lightbox did not open on image click"
            print("Lightbox modal opened successfully.")

            # Close lightbox via ESC
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(500)
            assert "active" not in (await lightbox.get_attribute("class")), "Lightbox did not close on Escape key"
            print("Lightbox closed via Escape key.")

            # 6. Test Right-Click Context Menu Suppression
            cm_prevented = await page.evaluate("""() => {
                let defaultPrevented = false;
                const event = new MouseEvent('contextmenu', {
                    bubbles: true,
                    cancelable: true,
                    view: window
                });
                defaultPrevented = !document.dispatchEvent(event);
                return defaultPrevented;
            }""")
            assert cm_prevented, "Context menu event was not prevented by main.js"
            print("Right-click context menu suppression verified.")

            # Take desktop screenshot
            await page.screenshot(path="test_results/desktop_view.png", full_page=True)
            print("Captured desktop view screenshot.")

            # Mobile viewport test
            mobile_context = await browser.new_context(viewport={'width': 375, 'height': 812})
            mobile_page = await mobile_context.new_page()
            await mobile_page.goto("http://localhost:8080/")
            await mobile_page.screenshot(path="test_results/mobile_view.png", full_page=True)
            print("Captured mobile view screenshot.")

            await browser.close()

            if console_errors:
                print("Console errors recorded:", console_errors)
            else:
                print("Zero console errors!")

    finally:
        server_process.terminate()

asyncio.run(main())
