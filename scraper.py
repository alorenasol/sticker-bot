import os
import requests
from playwright.sync_api import sync_playwright

URL = "https://jotform.com"
TARGET_KEYWORD = "Coca-Cola"
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

def send_discord_alert():
    if DISCORD_WEBHOOK_URL:
        payload = {"content": f"🚨 **PANINI ALERT!** The **{TARGET_KEYWORD}** stickers are now live on the form!\nBuy them here immediately: {URL}"}
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
    print("📨 Discord alert dispatched.")

def check_form():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            print("Navigating to Panini Point form...")
            page.goto(URL, wait_until="networkidle")
            
            page.click("text=Panini Point - Lincoln Plaza")
            page.click("text=MUNDIAL 2026")
            page.wait_for_timeout(3000)
            
            page_text = page.locator("body").inner_text()
            if TARGET_KEYWORD.lower() in page_text.lower():
                print("🎉 Keyword found!")
                send_discord_alert()
            else:
                print(f"ℹ️ Cleared. No sign of {TARGET_KEYWORD} yet.")
        except Exception as e:
            print(f"❌ Error navigating form: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    check_form()
