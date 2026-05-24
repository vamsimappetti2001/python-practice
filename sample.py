import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 1. Initialize the Chrome Driver
# The Service and ChromeDriverManager automatically manage the browser driver version
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # 2. Open Flipkart
    driver.get("https://www.flipkart.com")
    time.sleep(2) # Allow time for the page to load

    # 3. Locate the Search Bar
    # Flipkart's search input typically has the 'name' attribute set to 'q'
    search_bar = driver.find_element(By.NAME, "q")

    # 4. Perform Search
    search_bar.send_keys("Iphone 17 pro")
    search_bar.send_keys(Keys.ENTER)

    # 5. Wait for search results to load
    try:
        # Try to find product links in search results
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/p/')]"))
        )
        print("Search results loaded!")
        time.sleep(2)

        # 6. Select the first product from search results
        product_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")
        if product_links:
            first_product = product_links[0]
            first_product.click()
            print("Product selected!")
            time.sleep(3)  # Wait for product page to load
        else:
            raise Exception("No products found in search results")
    except Exception as e:
        print(f"Error finding products: {e}")
        print("Page source snippet for debugging:")
        page_source = driver.page_source
        # Print a portion of the page to help identify the correct selectors
        print(page_source[1000:2000])

    # 7. Wait for Add to Cart button to be clickable and click it
    try:
        add_to_cart_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add') or contains(@class, 'Add')]"))
        )
        add_to_cart_btn.click()
        print("Product added to cart!")
        time.sleep(2)
    except Exception as e:
        print(f"Error adding to cart: {e}")
        # Try alternative approach
        try:
            add_to_cart_alt = driver.find_element(By.XPATH, "//button[contains(., 'Add to Cart')]")
            add_to_cart_alt.click()
            print("Product added to cart (alternative method)!")
            time.sleep(2)
        except:
            print("Could not find Add to Cart button. Continuing anyway...")
            time.sleep(2)

    # 8. Navigate to cart
    try:
        driver.get("https://www.flipkart.com/viewcart")
        time.sleep(3)  # Wait for cart page to load
        print("Navigated to cart!")
    except Exception as e:
        print(f"Error navigating to cart: {e}")

    # 9. Click on Proceed to Checkout or Continue button
    try:
        checkout_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Proceed') or contains(., 'Continue') or contains(., 'Checkout')]"))
        )
        checkout_btn.click()
        print("Proceeding to checkout!")
        time.sleep(3)
    except Exception as e:
        print(f"Checkout button error: {e}")
        try:
            # Try clicking any button that might be checkout-related
            buttons = driver.find_elements(By.TAG_NAME, "button")
            for btn in buttons:
                if "proceed" in btn.text.lower() or "continue" in btn.text.lower():
                    btn.click()
                    print("Clicked checkout button (alternative method)!")
                    time.sleep(3)
                    break
        except:
            print("Could not find checkout button. Continuing anyway...")
            time.sleep(3)

    # 10. Wait for payment page to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Payment') or contains(text(), 'payment')]"))
        )
        print("Payment section reached!")
        time.sleep(3)
    except Exception as e:
        print(f"Could not confirm payment page load: {e}")
        print(f"Current URL: {driver.current_url}")
        time.sleep(3)

finally:
    # 6. Close the browser
    driver.quit()