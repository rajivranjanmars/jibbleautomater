import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Get credentials from environment variables (required)
user_email = os.getenv("JIBBLE_EMAIL")
password = os.getenv("JIBBLE_PASSWORD")

# Validate that credentials are provided
if not user_email or not password:
    raise ValueError("JIBBLE_EMAIL and JIBBLE_PASSWORD environment variables must be set")

# Configure Chrome options for GitHub Actions
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-running-insecure-content")


global driver

try:
    # Initialize Chrome driver
    driver = webdriver.Chrome(options=chrome_options)
    
    print("Navigating to Jibble login page...")
    driver.get("https://web.jibble.io/login")
    
    print("Entering credentials...")
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='emailOrPhone']"))
    )
    email_input.send_keys(user_email)
    
    password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
    password_input.send_keys(password)
    
    print("Clicking login button...")
    button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='login-button']")
    button.click()
    
    print("Waiting for login to complete...")
    # Wait for page to load and any dialogs to disappear
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "button"))
    )
    
    # Wait for any animations/dialogs to complete and handle overlays
    time.sleep(5)  # Increased wait time for animations
    
    # Try to dismiss any dialog overlays that might be blocking interactions
    try:
        # Wait for dialog backdrop to disappear
        WebDriverWait(driver, 15).until_not(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".q-dialog__backdrop"))
        )
        print("Dialog backdrop cleared")
    except:
        print("No dialog backdrop found or already cleared")
        
    # Also try to close any modal dialogs by pressing ESC
    try:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(2)
        print("Sent ESC key to close any dialogs")
    except:
        print("Could not send ESC key")
    
    print("Looking for clock-out button...")
    # Wait for clock-out button and ensure it's clickable
    clock_out_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='button-clock-out'][type='button']"))
    )
    print("clock_out_button found and clickable:", clock_out_button)
    
    # Use JavaScript click to bypass any overlay issues
    print("Using JavaScript click to avoid interception...")
    driver.execute_script("arguments[0].click();", clock_out_button)
    print("Clock-out button clicked via JavaScript")
    
    print("Waiting for save button...")
    # Wait a moment for the clock-out action to register
    time.sleep(3)
    
    # Click on the save button using JavaScript as well
    save_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid='right-sidebar-confirm-btn'][type='button']"))
    )
    print("save_button found:", save_button)
    
    # Use JavaScript click for save button too
    driver.execute_script("arguments[0].click();", save_button)
    print("Save button clicked via JavaScript")
    
    print("Successfully clocked out!")
    
except Exception as e:
    print(f"Error occurred: {str(e)}")
    if 'driver' in locals():
        driver.save_screenshot("error_screenshot.png")
    raise
finally:
    if 'driver' in locals():
        driver.quit()