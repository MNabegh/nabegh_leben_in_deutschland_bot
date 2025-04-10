import time
import logging
from datetime import datetime, timedelta
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# === Configuration ===
BOT_TOKEN = "7968429839:AAHrvQLKB7ovLTfuBPKck4SKyUvoCHC2oTE"       # Replace with your Telegram bot token
CHAT_ID = "1208408981"           # Replace with your personal chat ID

# === Logging Setup ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# === Telegram Notification Function (using requests) ===
def send_telegram_notification(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"  # You can change to HTML if needed
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        logging.info("Telegram notification sent successfully. Response: %s", response.text)
    except Exception as e:
        logging.error("Failed to send telegram message: %s", e)

# === Function to Check the Einbürgerungstest Page ===
def check_einbuergerungstest():
    url = "https://service.berlin.de/dienstleistung/351180/"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        logging.error("Error initializing WebDriver: %s", e)
        return False

    appointment_found = False
    try:
        driver.get(url)
        time.sleep(2)  # Allow the page to load

        # Locate and click the search button
        search_button = driver.find_element(By.CLASS_NAME, "button--negative")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_button)
        time.sleep(1)
        search_button.click()
        time.sleep(2)

        # Check if the "no appointments" message is present
        page_text = driver.page_source
        if "Leider sind aktuell keine Termine für ihre Auswahl verfügbar." in page_text:
            logging.info("No appointments available.")
        else:
            appointment_found = True
            logging.warning("Appointment available or unexpected page state detected!")
            send_telegram_notification(
                "🚨 *Appointment Alert!* An appointment was found on the Berlin Einbürgerungstest page! Please check immediately."
            )
    except Exception as e:
        logging.error("Error while checking the page: %s", e)
    finally:
        driver.quit()
    
    return appointment_found

# === Main Loop ===
if __name__ == "__main__":
    logging.info("Script started: Monitoring the Berlin Einbürgerungstest page.")
    send_telegram_notification("🟢 *Deployment Started:* The script is running and monitoring the Berlin Einbürgerungstest page.")

    last_heartbeat = datetime.now()

    while True:
        try:
            found = check_einbuergerungstest()
            if found:
                logging.info("Appointment found. Sleeping for 10 minutes before the next check.")
                time.sleep(600)  # Sleep for 10 minutes if an appointment is found

            # Send heartbeat notification every 24 hours
            if (datetime.now() - last_heartbeat) >= timedelta(hours=24):
                send_telegram_notification("✅ *Heartbeat:* The script is still running.")
                last_heartbeat = datetime.now()

        except Exception as e:
            logging.error("Unexpected error in main loop: %s", e)
        
        time.sleep(30)  # Wait 30 seconds before the next check
