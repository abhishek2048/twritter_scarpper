from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
import time

# MongoDB Configuration
client = MongoClient('mongodb+srv://Abhishek:DYvGt8z7jItKTnuL@abhishek.wcka65c.mongodb.net')
db = client.twitter_trends
collection = db.trends

# Twitter Credentials
TWITTER_USERNAME = "abhishek_13042"
TWITTER_PASSWORD = "abhishek2048"

# ProxyMesh Configuration
PROXY_URL = "http://abhishek2021:2021am28ab@45.32.86.6:31280"  # Replace with your ProxyMesh credentials

def setup_chrome():
    options = webdriver.ChromeOptions()
    options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Path to Chrome

    # Add ProxyMesh proxy settings
    options.add_argument(f'--proxy-server={PROXY_URL}')  # Use ProxyMesh

    options.add_argument('--disable-dev-shm-usage')  # Prevent resource issues
    options.add_argument('--no-sandbox')            # Avoid sandboxing issues
    options.add_argument('--disable-gpu')           # Disable GPU acceleration
    options.add_argument('--start-maximized')       # Start in maximized mode
    options.add_argument('--log-level=3')           # Suppress logs
    return webdriver.Chrome(options=options)

def scrape_twitter_trends():
    driver = None
    try:
        # Initialize WebDriver
        driver = setup_chrome()

        # Open Twitter login page
        driver.get('https://twitter.com/login')

        # Step 1: Enter Username and Press Enter
        try:
            username_field = WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.NAME, 'text'))
            )
            username_field.send_keys(TWITTER_USERNAME)
            username_field.send_keys(Keys.RETURN)  # Press Enter
        except Exception as e:
            print(f"Error entering username: {e}")
            driver.save_screenshot('error_username.png')  # Save screenshot for debugging
            time.sleep(180)  # Keep browser open for 3 minutes
            return

        # Step 2: Enter Password and Press Enter
        try:
            password_field = WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.NAME, 'password'))
            )
            password_field.send_keys(TWITTER_PASSWORD)
            password_field.send_keys(Keys.RETURN)  # Press Enter
        except Exception as e:
            print(f"Error entering password: {e}")
            driver.save_screenshot('error_password.png')  # Save screenshot for debugging
            time.sleep(180)  # Keep browser open for 3 minutes
            return

        # Wait for Home Page to Load
        time.sleep(30)

        # Scrape Twitter trends from "What’s happening" section
        try:
            trends_section = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//section[contains(@aria-labelledby, "accessible-list")]'))
            )
            trends = trends_section.find_elements(By.XPATH, './/span[contains(@class, "css-901oao")]')
            top_trends = [trend.text for trend in trends[:5] if trend.text.strip()]
        except Exception as e:
            print(f"Error scraping trends: {e}")
            driver.save_screenshot('error_trends.png')  # Save screenshot for debugging
            time.sleep(180)  # Keep browser open for 3 minutes
            return

        # Store in MongoDB
        data = {
            'trends': top_trends,
            'timestamp': time.time()
        }
        collection.insert_one(data)
        print("Data successfully inserted into MongoDB:", data)

        # Keep browser open for 3 minutes
        print("Browser will remain open for 3 minutes. Close it manually if needed.")
        time.sleep(180)

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    scrape_twitter_trends()
