import asyncio
import os
import subprocess
import time
from playwright.async_api import async_playwright

async def main():
    # Start local HTTP server
    server_proc = subprocess.Popen(["python3", "-m", "http.server", "8080"])
    time.sleep(1.5)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)

            # Desktop Verification
            page = await browser.new_page(viewport={"width": 1280, "height": 800})

            # Navigate to local page
            await page.goto("http://localhost:8080")

            # Screenshot 1: Midway through sweep animation
            await asyncio.sleep(1.2)
            await page.screenshot(path="screenshot_sweep_midway.png")
            print("Captured screenshot_sweep_midway.png")

            # Screenshot 2: Final settled layout
            await asyncio.sleep(2.0)
            await page.screenshot(path="screenshot_settled_final.png")
            print("Captured screenshot_settled_final.png")

            # Screenshot 3: Hover and interaction test on Google sign-in button
            await page.hover("#btn-google-auth")
            await page.screenshot(path="screenshot_google_hover.png")
            print("Captured screenshot_google_hover.png")

            # Mobile Viewport Verification
            mobile_page = await browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True)
            await mobile_page.goto("http://localhost:8080")
            await asyncio.sleep(3.0)
            await mobile_page.screenshot(path="screenshot_mobile.png")
            print("Captured screenshot_mobile.png")

            await browser.close()
    finally:
        server_proc.terminate()

if __name__ == "__main__":
    asyncio.run(main())
