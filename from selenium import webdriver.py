from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Initialize the Chrome WebDriver
# Note: Modern Selenium (v4.6+) automatically handles driver management
driver = webdriver.Chrome()

try:
    # 1. Navigate to a website
    driver.get("https://www.google.com")
    
    # 2. Maximize the window
    driver.maximize_window()
    
    # 3. Request information (get the page title)
    print(f"Page Title: {driver.title}")
    
    # Wait for 3 seconds to see the result
    time.sleep(3)

finally:
    # 4. Close the browser session
    driver.quit()
