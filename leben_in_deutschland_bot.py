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
