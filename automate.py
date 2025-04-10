import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests

def send_telegram_notification(message):
    bot_token = "7968429839:AAHrvQLKB7ovLTfuBPKck4SKyUvoCHC2oTE"  # Replace with your Telegram bot token
    chat_id = "1208408981"      # Replace with your chat ID
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print("Telegram notification sent successfully!")
    except requests.exceptions.RequestException as e:
        print("Failed to send Telegram message:", e)

def check_einbuergerungstest():
    # URL for the Einbürgerungstest service in Berlin
    url = "https://service.berlin.de/dienstleistung/351180/"

    # Configure Selenium (uncomment headless if you don't need a visible browser window)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Uncomment to run in headless mode
    chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize WebDriver (using Chrome in this example)
    driver = webdriver.Chrome(options=chrome_options)
    appointment_found = False  # Flag to determine if an appointment is available

    try:
        # Open the page
        driver.get(url)
        time.sleep(2)  # Wait for the page to load

        # 1) Click "Alle Standorte auswählen" checkbox
        #checkbox = driver.find_element(By.ID, "checkbox_overall")
        #driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
        #time.sleep(1)  # Allow some time for the scrolling
        #checkbox.click()
        #time.sleep(1)

        # 2) Click the button to search for appointments
        search_button = driver.find_element(By.CLASS_NAME, "button--negative")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_button)
        time.sleep(1)  # Allow some time for the scrolling

        search_button.click()
        time.sleep(2)  # Wait for the next page to load

        # 3) Check the page source for the specific text indicating no appointments
        page_text = driver.page_source

        if "Leider sind aktuell keine Termine für ihre Auswahl verfügbar." in page_text:
            print("No appointments available.")
        else:
            appointment_found = True
            print("Appointments available or text not found! Please check manually.")
            send_telegram_notification("!!!!!!!An appointment was found on the Berlin service website. Please check manually.")
            
    except Exception as e:
        print("An error occurred:", e)
    finally:
        # Only close the browser if no appointment was found
        if not appointment_found:
            driver.quit()
        else:
            time.sleep(600)
            
    return appointment_found

if __name__ == "__main__":
    while True:
        if check_einbuergerungstest():
            # Appointment found: break the loop so it won't run again.
            break
        time.sleep(30)
