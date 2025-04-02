# This test is to search for a playlist and extract the data from web
from selenium import webdriver
# This line is necesary for search the HTML elements
from selenium.webdriver.common.by import By
# Libraries for implicit waits
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json
import random
import os

# Obtener el directorio base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# load driver
driver = webdriver.Chrome()

# Open Spotify
driver.get("https://open.spotify.com/")
# Wait for  elements to load
driver.maximize_window()
wait = WebDriverWait(driver, 10)

# read the json with the songs and artists
json_path = os.path.join(BASE_DIR, 'files', 'Spotify_playlist_beginner.json')
with open(json_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

artists = set()
for song in data:
    artists.update(song["Artists"])

print(artists)

chosen_artists = random.sample(list(artists), 3)

print("The chosen artist to tesstare: ", chosen_artists)

body = driver.find_element(By.TAG_NAME, "body")
artists_data = []
# For each artists open a new tab and go down to click the artists infor and get the world position and, followers and top 5 cities.
for artist in chosen_artists:
    print("The artist to test is: ", artist)
    driver.switch_to.new_window("tab")
    driver.get("https://open.spotify.com/")
    searchBar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='search-input']")))
    searchBar.send_keys(artist + Keys.RETURN)
    artist_button = wait.until(EC.presence_of_element_located((By.XPATH, ".//a/button/span[text() = 'Artistas']")))
    artist_button.click()
    topArtist = wait.until(EC.presence_of_element_located((By.XPATH, f".//p[@title = '{artist}']")))
    print("The top artist is: ", topArtist.text)
    topArtist.click()
    time.sleep(3)

    for _ in range(50):
        try:
            artist_info_button = driver.find_element(By.XPATH, f".//button[@aria-label='{artist}']")
            print("Button found for artist: ", artist)
            break
        except:
            body.send_keys(Keys.PAGE_DOWN)

    if artist_info_button:
        artist_info_button.click()
        try:
            dialog = driver.find_element(By.XPATH, f".//dialog[@aria-label='{artist}']")
            data_container = dialog.find_element(By.XPATH, "//div[count(./div) = 9]")
            world_number = data_container.find_element(By.XPATH,"//div[count(following-sibling::div) = 8 ]/div[starts-with(.,'#')]").text.strip("#")
            followers = data_container.find_element(By.XPATH, "./div/div[not(translate(., '0123456789.', ''))]")[0].text.strip(".")
            mensual = data_container.find_element(By.XPATH, "./div/div[not(translate(., '0123456789.', ''))]")[1].text.strip(".")
            Cities = data_container.find_element(By.XPATH, "./div[child::div[1][translate(., '0123456789.#', '')]]")
            print("The artist: ", artist, "has: ", followers, "followers and is the number: ", world_number, "in the world")
            print("The artist: ", artist, "has: ", mensual, "monthly listeners")
            print("The artist: ", artist, "has: ", Cities, "followers in the cities")
            print("*"*100)
        except:
            print("Dialog not found")




