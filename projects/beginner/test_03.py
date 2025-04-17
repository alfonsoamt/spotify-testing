"""
This script reads artists from a JSON file, searches for each on Spotify in separate tabs, extracts specific data from their info dialogs, and saves it to a JSON file.

Selenium Concepts Covered:
*   Initializing and managing the WebDriver (`webdriver.Chrome`).
*   Navigation (`driver.get()`).
*   Managing multiple browser tabs/windows (`driver.switch_to.new_window("tab")`).
*   Locating elements using CSS Selectors and XPath.
*   Element interaction (`.click()`, `.send_keys()`).
*   Using explicit waits (`WebDriverWait`, `expected_conditions as EC`).
*   Handling `TimeoutException`.
*   Interacting with dialog boxes/modals.
*   Handling dynamically appearing elements.
*   Simulating page scrolling (`Keys.PAGE_DOWN`).
*   Extracting text from elements.
*   Reading data from a JSON file using the `json` library.
*   Saving data to a JSON file using the `json` library.

Test Actions Performed:
*   Reads song data from an external JSON file (`Spotify_playlist_beginner.json`).
*   Extracts unique artist names and selects a random sample (3 artists).
*   Initializes the WebDriver and navigates to Spotify.
*   For each selected artist:
    *   Opens a new browser tab and navigates to Spotify.
    *   Searches for the artist using the search bar.
    *   Filters results by clicking the 'Artists' button.
    *   Clicks on the top artist result matching the name.
    *   Scrolls down the artist's page until an 'About' or info button is found and clicks it.
    *   Waits for the artist information dialog to appear.
    *   Extracts data from the dialog: World Ranking (if available), Followers, Monthly Listeners, and Top 5 Cities.
    *   Stores the extracted data for the artist.
*   Saves the collected data for all processed artists into a new JSON file (`Spotify_artists_data.json`).
"""

# First import all the necessary libraries from selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
# Import the Selenium exceptions
from selenium.common.exceptions import TimeoutException
# Import the os library to access the environment variables
import os
# Import the json library to load the JSON data
import json
# Import the random library to select random elements from a list
import random

# Initialize the project path to save files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Initialize the path to save the screenshots
SCREENSHOTS_PATH = os.path.join(BASE_DIR, "screenshots", "beginner")
# Create the screenshots directory if it doesn't exist
os.makedirs(SCREENSHOTS_PATH, exist_ok=True)
# Initialize the path to load the JSON file
READ_JSON_PATH = os.path.join(BASE_DIR, "files", "Spotify_playlist_beginner.json")
# Create the JSON directory for save data if it doesn't exist
SAVE_JSON_PATH = os.path.join(BASE_DIR, "files")
os.makedirs(SAVE_JSON_PATH, exist_ok=True)
FILE_DATA_JSON = os.path.join(SAVE_JSON_PATH, "Spotify_artists_data.json")

# Initialize the default driver for Chrome
driver = None
try:
    # --- Block 1: Read the data from the JSON and select random data ---

    # Read the data from the JSON file
    print("INFO: Loading data from the JSON file...")
    try:
        with open(READ_JSON_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
        print("INFO: Data loaded successfully.")
        # Inialize the set to store the artists to avoid duplicates
        artists = set()
        for song in data:
            artists.update(song["Artists"])
        # Choose 3 random artists from the JSON file
        chosen_artists = random.sample(list(artists), 3)
    except FileNotFoundError as e_load_data:
        print(f"ERROR: JSON file not found: {e_load_data}")
        raise e_load_data
    else:
        print("DEBUG: From the JSON file, three artists were selected: ", chosen_artists)

    # --- Block 2: Initialize the WebDriver, open a new tab each chosen artist and look for the info page ---

    print("INFO: Initializing the WebDriver...")
    # Initialize the driver for Chrome
    driver = webdriver.Chrome()
    driver.get("https://open.spotify.com/")
    driver.maximize_window()

    # Create a wait object for the driver
    wait = WebDriverWait(driver, 10)
    # Variable to store the body element, this will be used to scroll down the page
    body = driver.find_element(By.TAG_NAME, "body")
    # Initialize the empty list to store the artists data
    artists_data = []
    all_artists_data = []
    # For each artists open a new tab and go down in the page to click the artists info and get the world position (if it exists), followers and top 5 cities.
    print("INFO: Starting to open new tabs and extract data...")
    for artist in chosen_artists:
        try:
            print("INFO: Opening new tab for artist: ", artist)
            # Open a new tab and go to the Spotify page
            driver.switch_to.new_window("tab")
            driver.get("https://open.spotify.com/")
            # Create variables to save the XPath locators for the elements
            SEARCHBAR_LOCATOR = "[data-testid='search-input']"
            ARTISTS_BUTTON_LOCATOR = ".//a/button/span[text() = 'Artistas']"
            TOP_ARTIST_LOCATOR = f".//p[@title = '{artist}']"
            ARTIST_INFO_BUTTON_LOCATOR = f".//button[@aria-label='{artist}']"
            DIALOG_LOCATOR = f".//dialog[@aria-label='{artist}']"
            DATA_CONTAINER_LOCATOR = f".//dialog[@aria-label='{artist}']//div[count(./div) >= 7]"
            WORLD_FOLLOWERS_MONTHLY_LISTENERS_LOCATOR = DATA_CONTAINER_LOCATOR + "//div[not(translate(., '0123456789.', ''))]"
            WORLD_NUMBER_LOCATOR = ".//div[count(following-sibling::div) >= 7 ]/div[starts-with(.,'#')]"
            CITIES_LOCATOR = WORLD_FOLLOWERS_MONTHLY_LISTENERS_LOCATOR + "/../following-sibling::div[position() <= 5]"
            # Wait for the search bar to be present and send the artist name to it
            searchBar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, SEARCHBAR_LOCATOR)))
            searchBar.send_keys(artist + Keys.RETURN)
            # Wait for the artists button to be present and click it
            artist_button = wait.until(EC.presence_of_element_located((By.XPATH, ARTISTS_BUTTON_LOCATOR)))
            artist_button.click()
            # Wait for the top artist to be present and click it
            topArtist = wait.until(EC.presence_of_element_located((By.XPATH, TOP_ARTIST_LOCATOR)))
            print("INFO: The top artist is: ", topArtist.text)
            topArtist.click()
            # Save the screenshot of the artist page
            driver.save_screenshot(os.path.join(SCREENSHOTS_PATH, f"artist_page_{artist}.png"))
            # Wait in the artist page, scroll down in a loop until to find the artist info button
            artist_info_button = None
            # If the artist info button is not found after 20 tries, continue to the next artist
            tries_count = 0
            while artist_info_button is None and tries_count < 20:
                artist_info_button = wait.until(EC.visibility_of_element_located((By.XPATH, ARTIST_INFO_BUTTON_LOCATOR)))
                if artist_info_button:
                    break
                else:
                    # Scroll down the page to load more elements
                    body.send_keys(Keys.PAGE_DOWN)
                    tries_count += 1

        except TimeoutException as e_artist_button:
            print(f"ERROR: Element not found: {e_artist_button}")
            raise e_artist_button
        else:
            if tries_count == 20:
                print(f"WARNING: Artist info button not found for {artist}. Skip this artist.")
                continue
            # If the artist info button is found, click it and get the data
            print(f"INFO: Artist info for {artist} found and opened successfully!")
            artist_info_button.click()
            # Save the screenshot of the artist info page
            print("INFO: Saving screenshot of the artist info page...")
            driver.save_screenshot(os.path.join(SCREENSHOTS_PATH, f"artist_info_page_{artist}.png"))

            # --- Block 3: Find the dialog element and get the data from each artist ---
            
        try:
            # Wait for the dialog element to be present
            dialog = wait.until(EC.presence_of_element_located((By.XPATH, DIALOG_LOCATOR)))
            print(f"DEBUG: Dialog found for {artist}.")
            # No wait for the data_container element to be present
            data_container = wait.until(EC.presence_of_element_located((By.XPATH, DATA_CONTAINER_LOCATOR)))
            print(f"DEBUG: Data container found for {artist}.")
            # Wait for the data container to not be empty
            wait.until(lambda d: data_container.text != "")
            # Get the interest elements from the data container
            world_number = data_container.find_elements(By.XPATH, WORLD_NUMBER_LOCATOR)
            # Verify if the list is not empty
            if world_number:
                world_number = world_number[0].text.strip("#")
                print(f"INFO: Ranking found for artist {artist}: ", world_number)
            else:
                world_number = "N/A"
                print("INFO: Ranking not found for artist: ", artist)
            # Get the followers and mensual elements from the data container
            followers  = wait.until(EC.presence_of_all_elements_located((By.XPATH, WORLD_FOLLOWERS_MONTHLY_LISTENERS_LOCATOR)))[0]
            print(f"INFO: Followers found for artist {artist}: ", followers.text.replace(".", ""))
            mensual_listeners = wait.until(EC.presence_of_all_elements_located((By.XPATH, WORLD_FOLLOWERS_MONTHLY_LISTENERS_LOCATOR)))[1]
            print(f"INFO: Mensual listeners found for artist {artist}: ", mensual_listeners.text.replace(".", ""))
            # Get the Top Cities elements from the data container
            cities_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, CITIES_LOCATOR)))
            # Extract the text from the elements
            cities_text = [city.text for city in cities_elements]
            # Verify if 5 cities were found
            if len(cities_text) == 5:
                print(f"INFO: These are the 5 Cities and their listeners:  {','.join(cities_text)}")
            else:
                print(f"WARNING: Less than 5 cities found for artist {artist}. Found: {len(cities_text)} cities {','.join(cities_text)}")

            # Create a dictionary with the data for the current artist
            current_artist_info = {
                "Artist": artist,
                "Ranking": world_number,
                "Followers": followers.text.replace(".", ""),
                "MonthlyListeners": mensual_listeners.text.replace(".", "")   ,
                "TopCities": cities_text 
            }
            # Append the current artist data to the list
            all_artists_data.append(current_artist_info)

        except TimeoutError as e_artist_info:
            print(f"ERROR: Timeout error: {e_artist_info}")
            raise e_artist_info
        else:
            print(f"INFO: Artist info for {artist} found and saved successfully!")
            
            # Save the data to a JSON file
            print("INFO: Saving data to JSON file...")
            with open(FILE_DATA_JSON, "w", encoding="utf-8") as file:
                json.dump(all_artists_data, file, indent=4, ensure_ascii=False)

            print(f"INFO: Data saved to {FILE_DATA_JSON} successfully!")
except Exception as e_unhandled:
    print(f"ERROR: Unhandled exception: {e_unhandled}")
    # Save the screenshot of the error
    if driver:
        try:    
            driver.save_screenshot(os.path.join(SCREENSHOTS_PATH, "unhandled_error_03.png"))
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
    print("INFO: Test finished successfully!")