"""This scripts contains the modular functions related to the web driver"""

# Import all the necessary libraries form Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager 
import logging

# Set up logging configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to create a Chrome WebDriver instance with specified options
def create_chrome_driver(headless: bool = False, incognito: bool = False, maximize: bool = False) -> webdriver.Chrome:
    """
    Create a Chrome WebDriver instance with specified options.

    Args:
        headless (bool): Run in headless mode if True.
        incognito (bool): Open in incognito mode if True.
        maximize (bool): Maximize the window if True.

    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance.
    """
    # Set up Chrome options and service
    logger.info(f"Creating Chrome WebDriver with headless={headless}, incognito={incognito}, maximize={maximize}")
    try:
        chrome_options = ChromeOptions()
        if headless:
            chrome_options.add_argument("--headless")
        if incognito:
            chrome_options.add_argument("--incognito")
        if maximize:
            chrome_options.add_argument("--start-maximized")
    
        chrome_service = ChromeService(ChromeDriverManager().install())
        # Create the Chrome WebDriver instance
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        logger.info("Chrome WebDriver created successfully.")
        return driver
    
    except Exception as e_chrome_driver:
        logger.error(f"Error creating Chrome driver: {e_chrome_driver}")
        raise e_chrome_driver
    
# Function to close the WebDriver instance
def close_driver(driver: webdriver.Chrome) -> None:
    """
    Close the WebDriver instance.

    Args:
        driver (webdriver.Chrome): The WebDriver instance to close.
    """
    logger.info("Closing the WebDriver instance.")
    try:
        driver.quit()
        logger.info("WebDriver closed successfully.")
    except Exception as e_close_driver:
        logger.error(f"Error closing the WebDriver, the driver is invalid or it is  already closed: {e_close_driver}")
        raise e_close_driver