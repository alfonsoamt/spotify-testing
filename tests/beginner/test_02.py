"""
This script searches for a specific Spotify playlist, scrolls down to load all its tracks, extracts track details, and saves the data into CSV and JSON files.

Selenium Concepts Covered:
*   Initializing and managing the WebDriver (`webdriver.Chrome`).
*   Navigation (`driver.get()`) and element location (CSS Selector, complex XPath).
*   Element interaction (`.click()`, `.send_keys()`).
*   Using explicit waits (`WebDriverWait`, `expected_conditions as EC`).
*   Handling `TimeoutException`.
*   Interacting with the DOM to extract data.
*   Simulating page scrolling using `Keys.PAGE_DOWN`.
*   Handling dynamically loaded content within a list/grid.
*   Extracting text and attributes from elements.

Test Actions Performed:
*   Navigates to the Spotify homepage.
*   Uses the search bar to find a specific playlist (`Top 50: México`).
*   Filters search results by clicking the 'Playlists' button.
*   Clicks on the target playlist from the search results.
*   Scrolls down the playlist page repeatedly until all tracks are loaded into the DOM.
*   Extracts the following details for each track: position, name, artist(s), reproductions count, album name, and duration.
*   Stores the extracted data.
*   Saves the collected track data into both a CSV file and a JSON file.
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
# Import the csv and json libraries to save the data on CSV and JSON
import csv
import json

# Initialize the project path to save files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Initialize the path to save the screenshots
SCREENSHOTS_PATH = os.path.join(BASE_DIR, "screenshots", "beginner")
# Create the screenshots directory if it doesn't exist
os.makedirs(SCREENSHOTS_PATH, exist_ok=True)
# Create the output directory variable
OUTPUT_DIR = os.path.join(BASE_DIR, 'files')
# Create the output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
# Create the CSV and JSON file paths
CSV_PATH = os.path.join(OUTPUT_DIR, "Spotify_playlist_beginner.csv")
JSON_PATH = os.path.join(OUTPUT_DIR, "Spotify_playlist_beginner.json")

# Playlist name to search
PLAYLIST_NAME = "Top 50: México"

# Initialize the driver for Chrome
driver = None
try:
    print("INFO: Initializing the WebDriver...")
    driver = webdriver.Chrome()
    driver.get("https://open.spotify.com/")
    driver.maximize_window()

    # Create a wait object for the driver
    wait = WebDriverWait(driver, 10)

    # Search for the searbar, print the placeholder and send the playlist name
    print("INFO: Searching for the search bar...")
    SEARCH_BAR_LOCATOR = "[data-testid='search-input']"
    searchBar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, SEARCH_BAR_LOCATOR)))
    print(f"INFO: Search bar found")
    print(f"INFO: Search bar placeholder: {searchBar.get_attribute('placeholder')}")

    # --- Block 1: Search for the playlist and explore the Page ---
    try:
        # Send the playlist name
        searchBar.send_keys(PLAYLIST_NAME + Keys.RETURN)

        # Save the screenshot of the search bar
        driver.save_screenshot(os.path.join(SCREENSHOTS_PATH, "search_bar_test02.png"))

        # Make the search more specific by clicking on the List button
        print("INFO: Clicking on the List button...")
        LIST_BUTTON_LOCATOR = ".//a/button/span[text() = 'Listas']"
        List_button = wait.until(EC.presence_of_element_located((By.XPATH, LIST_BUTTON_LOCATOR)))
        List_button.click()

        # Select the first playlist from the results, this should match the playlist name
        print("INFO: Selecting the first playlist from the results...")
        PLAYLIST_ELEMENT_LOCATOR = ".//p/span/span"
        first_playlist = wait.until(EC.presence_of_element_located((By.XPATH, PLAYLIST_ELEMENT_LOCATOR)))
        first_playlist.click()

        #Get the playlist title and take a screenshot of the page
        print("INFO: Getting the playlist title and taking a screenshot of the page...")
        PLAYLIST_TITLE_LOCATOR = "//span/h1"
        playlistTitle = wait.until(EC.presence_of_element_located((By.XPATH, PLAYLIST_TITLE_LOCATOR)))
        print(f"INFO: Playlist title: {playlistTitle.text}")
        driver.save_screenshot(os.path.join(SCREENSHOTS_PATH, "playlist_page_test02.png"))

    except TimeoutException as e_elements_not_found:
        print(f"ERROR: Elements not found: {e_elements_not_found}")
        raise e_elements_not_found
    else:
        print("INFO: Elements found and clicked successfully!")

    # --- Block 2: Scroll down to load and get the data from the page ---
    try:
        print("INFO: Scrolling down to load and get the data from the page...")
        SCROLL_DOWN_LOCATOR = "//div[@data-testid='tracklist-row']"
        scroll_down = wait.until(EC.presence_of_element_located((By.XPATH, SCROLL_DOWN_LOCATOR)))
        scroll_down.click()

        # Initialize the auxiliar variables to save the data
        all_data = []
        unique_elements = set()
        last_count = 0

        # Create variables to save the XPath locators
        SONG_LOCATOR = "//div[@data-testid='tracklist-row']"
        LIST_POSITION_LOCATOR = ".//div/div/div/span"
        SONG_NAME_LOCATOR = ".//div/div/div[following-sibling::span/span/a]"
        ARTISTS_LOCATOR = ".//div/following-sibling::span/span[a]"
        REPRODUCTIONS_LOCATOR = ".//div[3]/div"
        ALBUM_LOCATOR = ".//div/span/a"
        DURATION_LOCATOR = ".//div/div[following-sibling::button][not(*)]"  

        # Create a loop to scroll down and get the data from the page until the number of songs is the same after the scroll
        while True:
            # Save previous number of songs before getting the new ones
            previous_unique_elements_count = len(unique_elements)
            print(f"DEBUG: Previous unique elements count: {previous_unique_elements_count}")

            # Get the songs from the current page view
            current_available_songs = wait.until(EC.presence_of_all_elements_located((By.XPATH, SONG_LOCATOR)))
            print(f"DEBUG: Current available songs in the DOM: {len(current_available_songs)}")

            # Extract the data from the current page view songs
            for song in current_available_songs:
                try:
                    listPosition = song.find_element(By.XPATH, LIST_POSITION_LOCATOR).text
                    songName = song.find_element(By.XPATH, SONG_NAME_LOCATOR).text
                    artists = song.find_element(By.XPATH, ARTISTS_LOCATOR)
                    allArtist = [artist.strip() for artist in artists.text.split(',')]
                    reproductions = song.find_element(By.XPATH, REPRODUCTIONS_LOCATOR).text
                    album = song.find_element(By.XPATH, ALBUM_LOCATOR).text
                    duration = song.find_element(By.XPATH, DURATION_LOCATOR).text
                    # Create a key for the song
                    songKey = (songName, tuple(allArtist))

                    # If the song is not in the unique elements, add it to the all data and unique elements
                    if songKey not in unique_elements:
                        all_data.append((listPosition, songName, allArtist, reproductions, album, duration))
                        unique_elements.add(songKey)

                except TimeoutException as e_song_data:
                    print(f"WARNING: Something went wrong while extracting the song data: {e_song_data}. Skipping this song...")
                    continue


            # Make a new count of the unique elements
            current_unique_elements_count = len(unique_elements)
            print(f"DEBUG: Current unique elements count: {current_unique_elements_count}")

            # If the number of unique elements is the same as the previous count, break the loop
            if current_unique_elements_count == previous_unique_elements_count:
                print(f"INFO: No new songs found, breaking the loop and stopping the scroll...")
                break
            else:
                print(f"INFO: New songs found {current_unique_elements_count - previous_unique_elements_count}, continuing the loop...")
                # Make a scroll down
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
                wait.until(EC.visibility_of_all_elements_located((By.XPATH, SONG_LOCATOR)))

        

    except TimeoutException as e_scroll_down_elements:
        print(f"ERROR: Element not found: {e_scroll_down_elements}")
        raise e_scroll_down_elements
    else:
        print(f"INFO: Total songs found for the playlist: {len(all_data)}")
        print("INFO: Scroll down done, data loaded and extracted!")

    # --- Block 3: Save the data on CSV and JSON ---
    # Save the data on CSV
    try:
        print("INFO: Saving the data on CSV and JSON...")
        # Create the CSV file
        with open(CSV_PATH, "w", newline = "", encoding = "utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Ranking", "Song", "Artists", "Reproductions", "Album", "Duration"])
            csv_data = []
            for ranking, song, artists_list, reproductions, album, duration in all_data:
                artists_str = ", ".join(artists_list)
                csv_data.append((ranking, song, artists_str, reproductions, album, duration))
            writer.writerows(csv_data)

        print("INFO: Data saved on CSV")

        # Create the JSON file
        with open(JSON_PATH, "w", encoding = "utf-8") as file:
            json.dump([{
                "Ranking": ranking, 
                "Song": song, 
                "Artists": artists,
                "Reproductions": reproductions, 
                "Album": album, 
                "Duration": duration
            } for ranking, song, artists, reproductions, album, duration in all_data], 
            file, indent = 4, ensure_ascii=False)

        print("INFO: Data saved on Json")

    except FileNotFoundError as e_save_data:
        print(f"ERROR: File not found: {e_save_data}")
        raise e_save_data
    else:
        print("INFO: Data saved on CSV and JSON successfully!") 
            
except Exception as e_unhandled:
    print(f"ERROR: Unhandled exception: {e_unhandled}")
    # Save the screenshot of the error
    if driver:
        try:    
            driver.save_screenshot(os.path.join(SCREENSHOTS_PATH, "unhandled_error_02.png"))
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
