"""This test is to explore the web page and extract the data from web
* Complex XPath
* 
* Simulate a scroll down to load new data in the DOM

This test focuses on:
* Make a search
* Get the data from the search
* Save the data on CSV and JSON
"""
# This test is to search for a playlist and extract the data from web
from selenium import webdriver
# This line is necesary for search the HTML elements
from selenium.webdriver.common.by import By
# Libraries for implicit waits
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import csv
import json
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

playlistName = "Top 50: México"

# Search for the searbar
searchBar = driver.find_element(By.CSS_SELECTOR, "[data-testid='search-input']")
print(searchBar.get_attribute("placeholder"))

# Send playlist
searchBar.send_keys(playlistName + Keys.RETURN)

List_button = wait.until(EC.presence_of_element_located((By.XPATH, ".//a/button/span[text() = 'Listas']")))
List_button.click()
time.sleep(2)  # Esperar a que se cargue la lista

# Buscar todos los elementos y seleccionar el primero
playlist_elements = driver.find_elements(By.XPATH, ".//p/span/span")
if playlist_elements:
    playlist_button = playlist_elements[0]
    playlist_button.click()
else:
    raise Exception("No se encontró ningún elemento de playlist")

#Get the playlist title
playlistTitle = wait.until(EC.presence_of_element_located((By.XPATH, "//span/h1")))
print(playlistTitle.text)

# variable to collect the data
allData = []
uniqueElements = set()
lastCount = 0

# search for the container element
scrollContainer = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "main-view-container")))

while True:
    songs = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='tracklist-row']")))
    # count elements
    newSongs = 0
    for song in songs:
        listPosition = song.find_element(By.XPATH, ".//div/div/div/span").text
        songName = song.find_element(By.XPATH, ".//div/div/div[following-sibling::span/span/a]").text
        artists = song.find_element(By.XPATH, ".//div/following-sibling::span/span[a]")
        allArtist = [artist.strip() for artist in artists.text.split(',')]
        reproductions = song.find_element(By.XPATH, ".//div[3]/div").text
        album = song.find_element(By.XPATH, ".//div/span/a").text
        duration = song.find_element(By.XPATH, ".//div/div[following-sibling::button][not(*)]").text

        songKey = (songName, tuple(allArtist))

        if songKey not in uniqueElements:
            allData.append((listPosition, songName, allArtist, reproductions, album, duration))
            uniqueElements.add(songKey)
            newSongs += 1

    if newSongs == 0:
        break

    # make scroll down
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
    time.sleep(1)


    
    if len(songs) == lastCount:
        break
    lastCount = len(songs)
    

# Close browser
driver.quit()

# Save data
output_dir = os.path.join(BASE_DIR, 'files')
os.makedirs(output_dir, exist_ok=True)

csv_path = os.path.join(output_dir, "Spotify_playlist_beginner.csv")
with open(csv_path, "w", newline = "", encoding = "utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Ranking", "Song", "Artists", "Reproductions", "Album", "Duration"])
    csv_data = []
    for ranking, song, artists_list, reproductions, album, duration in allData:
        artists_str = ", ".join(artists_list)
        csv_data.append((ranking, song, artists_str, reproductions, album, duration))
    writer.writerows(csv_data)

print("Data saved on CSV")

json_path = os.path.join(output_dir, "Spotify_playlist_beginner.json")
with open(json_path, "w", encoding = "utf-8") as file:
    json.dump([{
        "Ranking": ranking, 
        "Song": song, 
        "Artists": artists,
        "Reproductions": reproductions, 
        "Album": album, 
        "Duration": duration
    } for ranking, song, artists, reproductions, album, duration in allData], 
    file, indent = 4, ensure_ascii=False)

print("Data saved on Json")