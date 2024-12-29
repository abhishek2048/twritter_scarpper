
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
import time
from dotenv import load_dotenv
import os


load_dotenv()


MONGODB_URL = os.getenv("MONGODB_URL")
client = MongoClient(MONGODB_URL)
db = client.twitter_trends
collection = db.trends


TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")


PROXY_URL = os.getenv("PROXY_URL")

def setup_chrome():
    options = webdriver.ChromeOptions()
    options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"  

  
    options.add_argument(f'--proxy-server={PROXY_URL}') 

    options.add_argument('--disable-dev-shm-usage')  
    options.add_argument('--no-sandbox')           
    options.add_argument('--disable-gpu')         
    options.add_argument('--start-maximized')      
    options.add_argument('--log-level=3')         
    return webdriver.Chrome(options=options)

def scrape_twitter_trends():
    driver = None
    try:
     
        driver = setup_chrome()

   
        driver.get('https://twitter.com/login')

        
        try:
            username_field = WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.NAME, 'text'))
            )
            username_field.send_keys(TWITTER_USERNAME)
            username_field.send_keys(Keys.RETURN)  
        except Exception as e:
            print(f"Error entering username: {e}")
            driver.save_screenshot('error_username.png')  
            time.sleep(180)  
            return

       
        try:
            password_field = WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.NAME, 'password'))
            )
            password_field.send_keys(TWITTER_PASSWORD)
            password_field.send_keys(Keys.RETURN)  
        except Exception as e:
            print(f"Error entering password: {e}")
            driver.save_screenshot('error_password.png')  
            time.sleep(180) 
            return

       
        time.sleep(30)

       
        try:
            trends_section = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//section[contains(@aria-labelledby, "accessible-list")]'))
            )
            trends = trends_section.find_elements(By.XPATH, './/span[contains(@class, "css-901oao")]')
            top_trends = [trend.text for trend in trends[:5] if trend.text.strip()]
        except Exception as e:
            print(f"Error scraping trends: {e}")
            driver.save_screenshot('error_trends.png')  
            time.sleep(180) 
            return

       
        data = {
            'trends': top_trends,
            'timestamp': time.time()
        }
        collection.insert_one(data)
        print("Data successfully inserted into MongoDB:", data)

        
        print("Browser will remain open for 3 minutes. Close it manually if needed.")
        time.sleep(180)

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    scrape_twitter_trends()
