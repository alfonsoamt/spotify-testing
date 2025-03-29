# This test is to search for a playlist and extract the data from web
import pickle
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

# load driver
driver = webdriver.Chrome()

# Open Spotify
driver.get("https://open.spotify.com/")
# Wait for  elements to load
driver.maximize_window()
wait = WebDriverWait(driver, 10)

# Load coockies
with open('../../cookies/cookies.pkl', 'rb') as file:
    cookies = pickle.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)

# Refresh the paage
driver.refresh()
# Verify the session
try:
    profileIcon = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='user-widget-link']")))
    print("Session is restore successful!")

except:
    print("The session was not restore")

# read the json with the songs and artists
with open("../../files/Spotify_playlist_beginner.json", "r") as file:
    data = json.load(file)

artists = set()
for song in data:
    artists.update(song["Artists"])

chosen_artists = random.sample(list(artists), 3)

print("The chosen artist to tesstare: ", chosen_artists)

body = driver.find_element(By.TAG_NAME, "body")
artists_data = []
# For each artists open a new tab and go down to click the artists infor and get the world position and, followers and top 5 cities.
for artist in chosen_artists:
    driver.switch_to.new_window("tab")
    driver.get("https://open.spotify.com/")
    searchBar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='search-input']")))
    searchBar.send_keys(artist + Keys.RETURN)
    topResultCard = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='top-result-card']")))
    topResultCard.click()

    for _ in range(30):
        try:
            artist_button = driver.find_element(By.XPATH, f".//button[@aria-label='{artist}']")
            print("Button found for artist: ", artist)
        except:
            body.send_keys(Keys.PAGE_DOWN)

    if artist_button:
        artist_button.click()
        try:
            dialog = driver.find_element(By.XPATH, f".//dialog[@aria-label='{artist}']")
            data_container = dialog.find_element(By.XPATH, "//div[count(./div) = 9]")
            world_number = data_container.find_element(By.XPATH,"//div[count(following-sibling::div) = 8 ]/div[starts-with(.,'#')]").text.strip("#")
            followers = data_container.find_element(By.XPATH, "./div/div[not(translate(., '0123456789.', ''))]")[0].text.strip(".")
            mensual = data_container.find_element(By.XPATH, "./div/div[not(translate(., '0123456789.', ''))]")[1].text.strip(".")
            Cities = data_container.find_element(By.XPATH, "./div[child::div[1][translate(., '0123456789.#', '')]]")
        except:
            print("Dialog not found")




