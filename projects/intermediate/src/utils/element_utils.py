"""This page contains utility functions for interacting with web elements using Selenium."""

# Import all the necessary libraries from Selenium
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
# import the necessary libraries for the project
from typing import Optional, List
import logging

# set up logging configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Constants values for the project
DEFAULT_TIMEOUT = 10

# Define function to find an element by its locator
def find_element(driver: WebDriver, locator: tuple, timeout: int = DEFAULT_TIMEOUT) -> Optional[WebElement]:
    """
    Find an element on the page using the provided locator.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        locator (tuple): A tuple containing the locator strategy and value (e.g., (By.ID, "element_id")).
        timeout (int): The maximum time to wait for the element to be found.

    Returns:
        WebElement: The web element if found, None otherwise.
    """
    logger.info(f"Finding element with locator: {locator}")
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located(locator))
        logger.info("Element found!")
        return element
    except (TimeoutException, NoSuchElementException) as e_not_found:
        logger.error(f"Element not found: {e_not_found}", exc_info=True)
        return None
    except Exception as e_unhandled:
        logger.error(f"Unhandled exception: {e_unhandled}", exc_info=True)
        return None
    
# Define function to find multiple elements by their locator
def find_elements(driver: WebDriver, locator: tuple, timeout: int = DEFAULT_TIMEOUT) -> List[WebElement]:
    """
    Find multiple elements on the page using the provided locator.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        locator (tuple): A tuple containing the locator strategy and value (e.g., (By.ID, "element_id")).
        timeout (int): The maximum time to wait for the elements to be found.

    Returns:
        List[WebElement]: A list of web elements if found, empty list otherwise.
    """
    logger.info(f"Finding elements with locator: {locator}")
    try:
        wait = WebDriverWait(driver, timeout)
        elements = wait.until(EC.presence_of_all_elements_located(locator))
        logger.info("Elements found!")
        return elements
    except (TimeoutException, NoSuchElementException) as e_not_found:
        logger.error(f"Elements not found: {e_not_found}", exc_info=True)
        return []
    except Exception as e_unhandled:
        logger.error(f"Unhandled exception: {e_unhandled}", exc_info=True)
        return []
    
# Define a function to make a click on an element
def click_element(driver: WebDriver, element: WebElement, timeout: int = DEFAULT_TIMEOUT) -> bool:
    """
    Click on a web element.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        element (WebElement): The web element to click on.
        timeout (int): The maximum time to wait for the element to be clickable.

    Returns:
        bool: True if the click was successful, False otherwise.
    """
    logger.info("Clicking on the element...")
    try:
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.element_to_be_clickable(element))
        element.click()
        logger.info("Element clicked!")
        return True
    except (TimeoutException, ElementClickInterceptedException, StaleElementReferenceException) as e_click_failed:
        logger.error(f"Click failed: {e_click_failed}", exc_info=True)
        return False
    except Exception as e_unhandled:
        logger.error(f"Unhandled exception during click: {e_unhandled}", exc_info=True)
        return False
    
# Define a function to send keys to an element
def send_keys_to_element(driver: WebDriver, element: WebElement, keys: str, clear_element: bool = True, timeout: int = DEFAULT_TIMEOUT) -> bool:
    """
    Send keys to a web element.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        element (WebElement): The web element to send keys to.
        keys (str): The keys to send to the element.
        clear_element (bool): Whether to clear the element before sending keys.
        timeout (int): The maximum time to wait for the element to be interactable.

    Returns:
        bool: True if the keys were sent successfully, False otherwise.
    """
    logger.debug(f"Sending keys {keys} to the element {element}...")
    element_to_send_keys = find_element(driver, element, timeout)
    if not element_to_send_keys:
        logger.error("Element not found for sending keys.")
        return False
    try:
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.element_to_be_clickable(element_to_send_keys))
        if clear_element:
            element_to_send_keys.clear()
        element_to_send_keys.send_keys(keys)
        logger.info("Keys sent successfully!")
        return True
    except (TimeoutException, StaleElementReferenceException) as e_send_keys_failed:
        logger.error(f"Sending keys failed: {e_send_keys_failed}", exc_info=True)
        return False
    except Exception as e_unhandled:
        logger.error(f"Unhandled exception during sending keys: {e_unhandled}", exc_info=True)
        return False

# Define a function to check if an element is visible
def is_element_visible(driver: WebDriver, element: WebElement, timeout: int = DEFAULT_TIMEOUT) -> bool:
    """
    Check if a web element is visible on the page.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        element (WebElement): The web element to check for visibility.
        timeout (int): The maximum time to wait for the element to be visible.

    Returns:
        bool: True if the element is visible, False otherwise.
    """
    logger.info("Checking if the element is visible...")
    try:
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.visibility_of(element))
        logger.info("Element is visible!")
        return True
    except (TimeoutException, StaleElementReferenceException) as e_not_visible:
        logger.error(f"Element not visible: {e_not_visible}", exc_info=True)
        return False
    except Exception as e_unhandled:
        logger.error(f"Unhandled exception during visibility check: {e_unhandled}", exc_info=True)
        return False
    
# Define a function to extract text from an element
def get_element_text(element: WebElement) -> Optional[str]:
    """
    Extract text from a web element.

    Args:
        element (WebElement): The web element to extract text from.

    Returns:
        str: The extracted text if successful, None otherwise.   
    """
    logger.info("Extracting text from the element...")
    try:
        text = element.text
        logger.info(f"Extracted text: {text}")
        return text
    except StaleElementReferenceException as e_stale:
        logger.error(f"Stale element reference: {e_stale}", exc_info=True)
        return None
    except Exception as e_unhandled:
        logger.error(f"Unhandled exception during text extraction: {e_unhandled}", exc_info=True)
        return None