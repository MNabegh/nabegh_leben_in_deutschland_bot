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

# === Telegram Notification Function ===
def send_telegram_notification(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        logging.info("Telegram notification sent successfully.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send Telegram notification: {e}")

# === Function to Check the Einbürgerungstest Page ===
def check_einbuergerungstest():
    url = "https://service.berlin.de/dienstleistung/351180/"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize the WebDriver
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        logging.error(f"Error initializing WebDriver: {e}")
        return False

    appointment_found = False
    try:
        driver.get(url)
        time.sleep(2)  # Wait for the page to load

        # Click the search button
        search_button = driver.find_element(By.CLASS_NAME, "button--negative")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_button)
        time.sleep(1)
        search_button.click()
        time.sleep(2)

        # Check the page for appointment text
        page_text = driver.page_source
        if "Leider sind aktuell keine Termine für ihre Auswahl verfügbar." in page_text:
            logging.info("No appointments available.")
        else:
            appointment_found = True
            logging.warning("Appointments available or unexpected page state detected!")
            send_telegram_notification("🚨 Appointment found on the Berlin Einbürgerungstest page! Please check immediately.")
    except Exception as e:
        logging.error(f"An error occurred while checking the page: {e}")
    finally:
        if appointment_found:
            logging.info("Keeping browser open due to appointment alert (waiting 10 minutes before closing).")
            time.sleep(600)  # Wait 10 minutes if an appointment is detected
        else:
            driver.quit()
    return appointment_found

# === Main Loop ===
if __name__ == "__main__":
    # Send a startup message and log that the script has started
    logging.info("Script started: Monitoring the Berlin Einbürgerungstest page.")
    send_telegram_notification("🟢 Deployment started: The script is running and monitoring the Berlin Einbürgerungstest page.")

    # Track time for heartbeat messages
    last_heartbeat = datetime.now()

    while True:
        try:
            if check_einbuergerungstest():
                # If an appointment is found, break out of the loop.
                break

            # Send heartbeat every 24 hours
            if (datetime.now() - last_heartbeat) >= timedelta(hours=24):
                send_telegram_notification("✅ Heartbeat: The script is still running.")
                last_heartbeat = datetime.now()

        except Exception as e:
            logging.error(f"Unexpected error in main loop: {e}")

        # Wait 30 seconds before checking again
        time.sleep(30)
