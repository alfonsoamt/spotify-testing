"This page contains the modular functions related to authentication and user management."

# Import all the necessary libraries form Selenium
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
# Import the necessary libraries for the project 
import pickle
import os
import logging

# Set up logging configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants values for the project
DEFAULT_TIMEOUT = 10
LOGIN_URL = "https://accounts.spotify.com/en/login?allow_password=1"
USERNAME_INPUT = (By.ID, "login-username")
PASSWORD_INPUT = (By.ID, "login-password")
LOGIN_BUTTON = (By.ID, "login-button")
LOGGED_IN_INDICATOR = (By.CSS_SELECTOR, "button[data-testid='user-widget-link']")
LOGOUT_BUTTON = (By.CSS_SELECTOR, "button[data-testid='user-widget-dropdown-logout']")
BASE_URL = "https://www.spotify.com/"

def login_with_credentials(driver: WebDriver, username: str, password: str) -> bool:
    """
    Log in to Sptofy using the provided username and password.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        username (str): The Spotify username.
        password (str): The Spotify password.

    Returns:
        bool: True if login was successful, False otherwise.
    """
    logger.info("Logging in to Spotify...")
    try:
        driver.get(LOGIN_URL)
        wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
        # Wait for the username input field to be present and enter the username
        username_input = wait.until(EC.presence_of_element_located(USERNAME_INPUT))
        username_input.clear()
        username_input.send_keys(username)
        logger.info("Username entered.")
        # Wait for the password input field to be present and enter the password
        password_input = wait.until(EC.presence_of_element_located(PASSWORD_INPUT))
        password_input.clear()
        password_input.send_keys(password)
        logger.info("Password entered.")
        # Wait for the login button to be present and click it
        login_button = wait.until(EC.element_to_be_clickable(LOGIN_BUTTON))
        login_button.click()
        logger.info("Login button clicked.")
        # Verify the loging
        if is_logged_in(driver, timeout = 15):
            logger.info("Login successful.")
            return True
        else:
            logger.error("Validation failed: User is not logged in.")
            return False

    except TimeoutException as e_timeout:
        logger.error(f"Timeout while waiting for login elements: {e_timeout}", exc_info = True)
        return False
    except NoSuchElementException as e_no_element:
        logger.error(f"Element not found during login: {e_no_element}", exc_info = True)
        return False
    except WebDriverException as e_webdriver:
        logger.error(f"WebDriver error during login: {e_webdriver}", exc_info = True)
        return False
    except Exception as e_unexpected:
        logger.error(f"Unexpected error during login: {e_unexpected}", exc_info = True)
        return False


def is_logged_in(driver: WebDriver, timeout: int = DEFAULT_TIMEOUT) -> bool:
    """
    Check if the user is logged in to Spotify.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        timeout (int): The timeout value for waiting for elements.

    Returns:
        bool: True if logged in, False otherwise.
    """
    logger.info("Checking if user is logged in...")
    try:
        wait = WebDriverWait(driver, timeout)
        # Wait for the logged-in indicator to be present
        wait.until(EC.presence_of_element_located(LOGGED_IN_INDICATOR))
        logger.info("User is logged in.")
        return True
    
    except (TimeoutException, NoSuchElementException) as e_failed_loging:
        logger.error(f"User is not logged in: {e_failed_loging}", exc_info = True)
        return False
    except Exception as e_unexpected:
        logger.error(f"Unexpected error while checking login status: {e_unexpected}", exc_info = True)
        return False
    
def save_cookies(driver: WebDriver, filename_path: str) -> None:
    """
    Save the cookies of the current session to a file.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        filename_path (str): The path to the file where cookies will be saved.
    """
    logger.info(f"Saving cookies on: {filename_path} ...")
    try:
        # Verify the directory exists, if not create it
        os.makedirs(os.path.dirname(filename_path), exist_ok=True)
        # Save cookies to the specified file
        cookies = driver.get_cookies()
        with open(filename_path, "wb") as file:
            pickle.dump(cookies, file)
        logger.info("Cookies saved successfully.")

    except FileNotFoundError as e_file:
        logger.error(f"File not found: {e_file}", exc_info = True)
    except WebDriverException as e_webdriver:
        logger.error(f"WebDriver error while saving cookies: {e_webdriver}", exc_info = True)
    except Exception as e_unexpected:
        logger.error(f"Unexpected error while saving cookies: {e_unexpected}", exc_info = True)

def load_cookies(driver: WebDriver, filename_path: str) -> bool:
    """
    Load cookies from a file and add them to the current session.
    Remember to navigate to the base URL before loading cookies.
    This function also refreshes the page to ensure the cookies are applied.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        filename_path (str): The path to the file where cookies are saved.
    
    Returns:
        bool: True if cookies were loaded successfully, False otherwise.
    """
    logger.info(f"Loading cookies from: {filename_path} ...")
    try:
        # Open the file and load the cookies
        with open(filename_path, "rb") as file:
            cookies = pickle.load(file)

        # Go to the base URL before adding cookies
        logger.info(f"Navigating to base URL {BASE_URL} before loading cookies...")
        driver.get(BASE_URL)
        logger.info("Adding cookies to the browser...")

        # Add each cookie to the current session
        for cookie in cookies:
            driver.add_cookie(cookie)

        logger.info("Cookies added successfully.")
        # Refresh the page to apply the cookies
        driver.refresh()
        logger.info("Page refreshed after loading cookies.")
        return True

    except FileNotFoundError as e_file:
        logger.error(f"File not found: {e_file}", exc_info = True)
    except WebDriverException as e_webdriver:
        logger.error(f"WebDriver error while loading cookies: {e_webdriver}", exc_info = True)
    except Exception as e_unexpected:
        logger.error(f"Unexpected error while loading cookies: {e_unexpected}", exc_info = True)

def logout(driver: WebDriver) -> bool:
    """
    Log out from Spotify.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.

    Returns:
        bool: True if logout was successful, False otherwise.
    """
    logger.info("Logging out from Spotify...")

    if not is_logged_in(driver):
        logger.warning("User is not logged in, cannot log out.")
        return False
    try:
        wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
        # Click the logged-in indicator to open the dropdown menu
        logged_in_indicator = wait.until(EC.element_to_be_clickable(LOGGED_IN_INDICATOR))
        logged_in_indicator.click()
        # Click the logout button in the dropdown menu
        logger.info("Clicking the logout button...")
        logout_button = wait.until(EC.element_to_be_clickable(LOGOUT_BUTTON))
        logout_button.click()
        logger.info("Logout button clicked.")

        # Verify the logout by checking if the login indicator is no longer present
        if not is_logged_in(driver, timeout = 5):

            logger.info("Logout successful.")
            return True
        else:
            logger.error("Logout failed: User is still logged in.")
            return False        

    except TimeoutException as e_timeout:
        logger.error(f"Timeout while waiting for logout elements: {e_timeout}", exc_info = True)
        return False
    except NoSuchElementException as e_no_element:
        logger.error(f"Element not found during logout: {e_no_element}", exc_info = True)
        return False
    except WebDriverException as e_webdriver:
        logger.error(f"WebDriver error during logout: {e_webdriver}", exc_info = True)
        return False
    except Exception as e_unexpected:
        logger.error(f"Unexpected error during logout: {e_unexpected}", exc_info = True)
        return False    