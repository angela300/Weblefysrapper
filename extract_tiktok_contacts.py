# from playwright.sync_api import sync_playwright
# import time
# import random
# import json

# OUTPUT_FILE = "data/tiktok_results.json"

# # -----------------------------
# # Human-like delay
# # -----------------------------
# def human_delay(min_sec=2, max_sec=5):
#     time.sleep(random.uniform(min_sec, max_sec))


# # -----------------------------
# # Close TikTok login popup
# # -----------------------------
# def close_popup(page):
#     try:
#         # Press ESC (works often)
#         page.keyboard.press("Escape")
#         time.sleep(2)

#         # Try clicking buttons like "Not now"
#         buttons = page.query_selector_all("button")
#         for btn in buttons:
#             try:
#                 text = btn.inner_text().lower()
#                 if "not now" in text or "cancel" in text:
#                     btn.click()
#                     time.sleep(2)
#                     break
#             except:
#                 continue
#     except:
#         pass


# # -----------------------------
# # Main scraping function
# # -----------------------------
# def scrape():
#     results = []

#     with sync_playwright() as p:
#         browser = p.chromium.launch(
#             headless=False,
#             args=["--disable-blink-features=AutomationControlled"]
#         )

#         context = browser.new_context(
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
#         )

#         page = context.new_page()

#         # Step 1: Open TikTok search
#         query = "skincare kenya"
#         page.goto(f"https://www.tiktok.com/search?q={query}")
#         human_delay(5, 8)

#         print("Page loaded...")

#         # Step 2: Close popup if present
#         close_popup(page)

#         # Step 3: Scroll to load results
#         print("Scrolling...")
#         for _ in range(10):
#             page.mouse.wheel(0, 3000)
#             human_delay()

#         # Step 4: Collect profile links
#         print("Collecting profile links...")
#         links = set()

#         anchors = page.query_selector_all("a")
#         for a in anchors:
#             href = a.get_attribute("href")
#             if href and "/@" in href:
#                 clean_link = href.split("?")[0]
#                 links.add(clean_link)

#         print(f"Collected {len(links)} profile links")

#         # Step 5: Visit profiles (SMALL BATCH)
#         print("Visiting profiles...")
#         for link in list(links)[:40]:
#             try:
#                 page.goto(link)
#                 human_delay(3, 6)

#                 close_popup(page)

#                 # Extract bio
#                 bio = ""
#                 try:
#                     bio = page.locator("h2").inner_text()
#                 except:
#                     pass

#                 results.append({
#                     "url": link,
#                     "bio": bio
#                 })

#                 print(f"Scraped: {link}")

#             except Exception as e:
#                 print(f"Error: {e}")

#         browser.close()

#     # Step 6: Save results
#     with open(OUTPUT_FILE, "w") as f:
#         json.dump(results, f, indent=2)

#     print(f"\nSaved {len(results)} profiles to {OUTPUT_FILE}")


# # -----------------------------
# # Run
# # -----------------------------
# if __name__ == "__main__":
#     scrape()