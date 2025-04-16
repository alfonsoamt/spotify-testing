"""
This script performs a login on Spotify, saves the session cookies, and then restores the session using the saved cookies.

Selenium Concepts Covered:
*   Initializing and managing the WebDriver (`webdriver.Chrome`).
*   Basic navigation (`driver.get()`).
*   Closing the browser (`driver.quit()`).
*   Locating elements using different strategies (ID, CSS Selector).
*   Performing basic actions on elements (`.click()`, `.send_keys()`).
*   Using explicit waits (`WebDriverWait`, `expected_conditions as EC`).
*   Handling common Selenium exceptions (`TimeoutException`).
*   Managing browser cookies (`driver.get_cookies()`, `driver.add_cookie()`).
*   Saving and loading cookies using the `pickle` library.

Test Actions Performed:
*   Navigates to the Spotify login page.
*   Enters username and password credentials (loaded from environment variables).
*   Clicks the login button.
*   Verifies successful login by checking for the presence of the user profile icon.
*   Saves the current browser cookies to a file.
*   Closes the browser.
*   Opens a new browser instance.
*   Navigates back to Spotify.
*   Loads the saved cookies into the new browser session.
*   Refreshes the page.
*   Verifies successful login again by checking for the user profile icon.
"""

# First import all the necessary libraries from selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Import the Selenium exceptions
from selenium.common.exceptions import TimeoutException
# Import the dotenv library to load the environment variables
from dotenv import load_dotenv
# Import the os library to access the environment variables
import os
# Import the pickle library to save and load cookies
import pickle

# Load the environment variables
load_dotenv()
# Save login variables to use in script
username = os.getenv("LOGIN_USER")
password = os.getenv("LOGIN_PASSWORD")

# Initialize the project path to save files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# initialize the path to save the screenshots
SCREENSHOTS_PATH = os.path.join(BASE_DIR, "screenshots", "beginner")

# Create the screenshots directory if it doesn't exist
os.makedirs(SCREENSHOTS_PATH, exist_ok=True)

# Initialize the driver for Chrome
driver = None
try:
    print("INFO: Initializing the WebDriver...")
    driver = webdriver.Chrome()
    driver.get("https://open.spotify.com/")
    driver.maximize_window()

    # Create a wait object for the driver
    wait = WebDriverWait(driver, 10)   
    # Print info about the page
    print(f"INFO: Page title: {driver.title}")
    print(f"INFO: Page URL: {driver.current_url}")
    # Save the screenshot of the page
    driver.save_screenshot(os.path.join(SCREENSHOTS_PATH, "login_page_before_input_test01.png"))

    print("INFO: Searching for the login button...")
    LOGIN_ACCESS_BUTTON_LOCATOR = "[data-testid='login-button']"
    # Search for the login button
    login_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, LOGIN_ACCESS_BUTTON_LOCATOR)))
    print(f"INFO: Login access button found")
    # Click on the login button
    login_button.click()

    #Save the screenshot of the login page
    driver.save_screenshot(os.path.join(SCREENSHOTS_PATH, "login_page_before_input_test01.png"))

    # --- Block 1: Search for the username, password and login button ---
    try:
        # Search for the username input field
        print("INFO: Searching for the username input field...")
        LOGIN_USERNAME_LOCATOR = "login-username"
        username_input = wait.until(EC.presence_of_element_located((By.ID, LOGIN_USERNAME_LOCATOR)))
        print(f"INFO: Username input field found")
        # Send the username to the input field
        username_input.send_keys(username)
    
        # Search for the password input field
        print("INFO: Searching for the password input field...")
        LOGIN_PASSWORD_LOCATOR = "login-password"
        password_input = wait.until(EC.presence_of_element_located((By.ID, LOGIN_PASSWORD_LOCATOR)))
        print(f"INFO: Password input field found")
        # Send the password to the input field
        password_input.send_keys(password)  
        
        # Find the login button
        print("INFO: Searching for the login button...")
        LOGIN_BUTTON_LOCATOR = "login-button"
        login_button = wait.until(EC.element_to_be_clickable((By.ID, LOGIN_BUTTON_LOCATOR)))
        print(f"INFO: Login button found")
        # Click on the login button
        login_button.click()
    except TimeoutException as e_login_button:
        print(f"ERROR: Element not found: {e_login_button}")
        raise e_login_button
    else:
        print("INFO: Credentials sent and login button clicked successfully!")
        
    # Save the screenshot of the login page
    driver.save_screenshot(os.path.join(SCREENSHOTS_PATH, "login_page_after_input_test01.png")) 

    # --- Block 2: Verify login was successful and save the cookies ---
    USER_WIDGET_LINK_LOCATOR = "[data-testid='user-widget-link']"
    try:
        # Search for the profile icon
        print("INFO: Searching for the profile icon...")
        profile_icon = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, USER_WIDGET_LINK_LOCATOR)))
        print(f"INFO: Profile icon found, login successful!")
        # Save the cookies for the session
        with open(os.path.join(BASE_DIR, "cookies", "cookies.pkl"), "wb") as file:
            pickle.dump(driver.get_cookies(), file)
    except TimeoutException as e_profile_icon:
        print(f"ERROR: Profile icon not found: {e_profile_icon}")
        raise e_profile_icon
    else:
        print(f"INFO: Profile icon found, login successful, cookies saved!")

    # Save the screenshot of the login page
    driver.save_screenshot(os.path.join(SCREENSHOTS_PATH, "login_page_after_session_restored_test01.png"))

    # --- Block 3: Load the cookies and restore the session ---
    # To test the cookies, we need to load the cookies.Before, the browser need to be closed
    driver.quit()


    # Load the cookies
    print("INFO: Closing and opening the WebDriver to load the sesion...")
    driver = webdriver.Chrome()
    driver.get("https://open.spotify.com/")
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    try:
        with open(os.path.join(BASE_DIR, "cookies", "cookies.pkl"), "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        # Refresh the page
        driver.refresh()
        print("INFO: Cookies loaded successfully!")
        # Verify login was successful
        print("INFO: Searching for the profile icon...")
        USER_WIDGET_LINK_LOCATOR = "[data-testid='user-widget-link']"
        profile_icon = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, USER_WIDGET_LINK_LOCATOR)))
        print("INFO: Profile icon found, login successful!")
    except (FileNotFoundError, pickle.UnpicklingError) as e_load_cookies:
        print(f"ERROR: Cookies not loaded session not restored: {e_load_cookies}")
        raise e_load_cookies
    else:
        print("INFO: Cookies loaded and session restored successfully!")
        
    # Save the screenshot of the login page 
    driver.save_screenshot(os.path.join(SCREENSHOTS_PATH, "login_page_after_session_restored_test01.png"))

# Handle unhandled exceptions
except Exception as e_unhandled:
    print(f"ERROR: Unhandled exception: {e_unhandled}")
    # Save the screenshot of the error
    if driver:
        try:    
            driver.save_screenshot(os.path.join(SCREENSHOTS_PATH, "unhandled_error_01.png"))
        except Exception as e_screenshot:
            print(f"WARNING: Unhandled exception: {e_screenshot}")
    raise e_unhandled

# Finally block for cleanup
finally:
    print("INFO: finally block execution for cleanup...")
    if driver:
        print("INFO: Closing the browser...")
        driver.quit()
    else:
        print("WARNING: Browser was not initialized.")
    print("INFO: Test completed.")