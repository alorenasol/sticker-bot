import os
import requests
from playwright.sync_api import sync_playwright

URL = "https://jotform.com"
# We now watch out for both formatting possibilities!
TARGET_1 = "Coca-Cola"
TARGET_2 = "Coca Cola"

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

def send_discord_alert(found_keyword):
    if DISCORD_WEBHOOK_URL:
        payload = {
            "content": f"🚨 **PANINI ALERT!** The **{found_keyword}** stickers are now live on the form!\nBuy them here immediately: {URL}"
        }
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
    print(f"📨 Discord alert dispatched for {found_keyword}.")

def check_form():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            print("Navigating to Panini Point form...")
            page.goto(URL, wait_until="networkidle")
            
            # Navigate past the landing selections
            page.click("text=Panini Point - Lincoln Plaza")
            page.click("text=MUNDIAL 2026")
            page.wait_for_timeout(3000) # Give Jotform a moment to render elements
            
            # Read all generated text on the expanded sheet
            page_text = page.locator("body").inner_text().lower()
            
            # Check for either variation
            if TARGET_1.lower() in page_text:
                print(f"🎉 Found variation: {TARGET_1}")
                send_discord_alert(TARGET_1)
            elif TARGET_2.lower() in page_text:
                print(f"🎉 Found variation: {TARGET_2}")
                send_discord_alert(TARGET_2)
            else:
                print("ℹ️ Cleared. No matching Coca-Cola items available yet.")
                
        except Exception as e:
            print(f"❌ Error navigating form: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    check_form()
