from playwright.sync_api import sync_playwright
import time, random, json, os, urllib.parse


OUTPUT_FILE = "data/tiktok_results.json"
TARGET_PROFILES = 1200

# -----------------------------
# Human-like delay
# -----------------------------
def human_delay(min_sec=2, max_sec=5):
    time.sleep(random.uniform(min_sec, max_sec))

# -----------------------------
# Safe navigation
# -----------------------------
def safe_goto(page, url, retries=3):
    for attempt in range(retries):
        try:
            page.goto(url, timeout=60000, wait_until="domcontentloaded")
            return True
        except Exception as e:
            print(f"⚠️ Retry {attempt+1} failed: {e}")
            time.sleep(5)
    return False

# -----------------------------
# Close popups
# -----------------------------
def close_popup(page):
    try:
        page.keyboard.press("Escape")
        time.sleep(1)
        for btn in page.query_selector_all("button"):
            try:
                text = btn.inner_text().lower()
                if "not now" in text or "cancel" in text:
                    btn.click()
                    time.sleep(1)
                    break
            except:
                continue
    except:
        pass

# -----------------------------
# Clean profile URL
# -----------------------------
def clean_profile_url(href):
    if not href or "/@" not in href:
        return None

    href = href.split("?")[0]

    if "/video/" in href:
        return None

    if href.startswith("/"):
        href = "https://www.tiktok.com" + href

    try:
        username = href.split("/@")[1].split("/")[0]
        if not username:
            return None
        return f"https://www.tiktok.com/@{username}"
    except:
        return None

# -----------------------------
# Load existing profiles
# -----------------------------
def load_existing_profiles():
    if not os.path.exists(OUTPUT_FILE):
        return []
    with open(OUTPUT_FILE, "r") as f:
        return json.load(f)

# -----------------------------
# Save results
# -----------------------------
def save_results(results):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2)

# -----------------------------
# Main scraper
# -----------------------------
def scrape():
    existing_data = load_existing_profiles()
    existing_urls = set([item["url"] for item in existing_data])
    results = existing_data.copy()

    USER_DATA_DIR = os.path.join(os.getcwd(), "tiktok_session")

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            USER_DATA_DIR,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )

        page = context.new_page()

        # Manual login
        print("Opening TikTok...")
        
        input("👉 Log in manually, then press ENTER to continue...")

        queries = [
            "crypto trader usa",
            "cryptocurrency signals",
            "day trading crypto",
            "crypto beginner tips",
            "altcoin trading",
            "crypto youtube trader",
            "binance trading strategy",
            "ethereum investor",
            "crypto discord signals"
        ]

        no_progress_rounds = 0

        for query in queries:
            if len(results) >= TARGET_PROFILES:
                break

            encoded_query = urllib.parse.quote(query)
            url = f"https://www.tiktok.com/search?q={encoded_query}"

            print(f"\n🔎 Searching: {query}")

            if not safe_goto(page, url):
                print("❌ Failed to load search page")
                continue

            time.sleep(5)
            close_popup(page)

            links = set()
            last_height = 0
            scroll_count = 0

            print("Scrolling and collecting links...")

            while True:
                page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                human_delay(2, 4)
                scroll_count += 1

                anchors = page.query_selector_all('a[href*="/@"]')
                for a in anchors:
                    href = a.get_attribute("href")
                    clean_link = clean_profile_url(href)

                    if clean_link and clean_link not in existing_urls:
                        links.add(clean_link)

                print(f"Collected so far: {len(links)} links")

                new_height = page.evaluate("document.body.scrollHeight")

                if new_height == last_height or scroll_count > 80:
                    print("No more new results...")
                    break

                last_height = new_height

            print(f"Collected {len(links)} raw links")

            new_links_added = 0

            print("Saving collected links...")

            for link in links:
                if len(results) >= TARGET_PROFILES:
                    break

                if link not in existing_urls:
                    results.append({
                        "url": link
                    })
                    existing_urls.add(link)
                    new_links_added += 1

                    print(f"✅ {link}")

            # Detect no progress
            if new_links_added == 0:
                no_progress_rounds += 1
                print(f"⚠️ No new links from: {query}")
            else:
                no_progress_rounds = 0

            # Stop if exhausted
            if no_progress_rounds >= 3:
                print("🚫 No more results across queries. Stopping...")
                break

        save_results(results)

        print(f"\n🎉 Total profiles saved: {len(results)}")

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    scrape()
