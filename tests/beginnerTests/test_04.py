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
import csv
import json

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


playlistName = "Top 50: México"

# Search for the searbar
searchBar = driver.find_element(By.CSS_SELECTOR, "[data-testid='search-input']")
print(searchBar.get_attribute("placeholder"))

# Send playlist
searchBar.send_keys(playlistName + Keys.RETURN)

topResultCard = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='top-result-card']")))
topResultCard.click()


#Get the playlist title
playlistTitle = wait.until(EC.presence_of_element_located((By.XPATH, f"//h1[normalize-space(translate(text(), '\u00A0', ' '))='{playlistName}']")))
print(playlistTitle.text)

if playlistName == playlistTitle.text:
    print("Got the correct playlist")
else:
    print("Something went wrong with the playlist")

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
        allArtist = artists.text.strip()
        reproductions = song.find_element(By.XPATH, ".//div[3]/div").text
        album = song.find_element(By.XPATH, ".//div/span/a").text
        duration = song.find_element(By.XPATH, ".//div/div[following-sibling::button][not(*)]").text

        songKey = (songName, artists)

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
with open("../../files/Spotify_playlist_beginner.csv", "w", newline = "", encoding = "utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Ranking", "Song", "Artists", "Reproductions", "Album", "Duration"])
    writer.writerows(allData)

print("Data saved on CSV")

with open("../../files/Spotify_playlist_beginner.json", "w", encoding = "utf-8") as file:
    json.dump([{"Ranking": ranking, "Song": song, "Artists": artists, "Reproductions": reproductions, "Album": album, "Duration": duration} for ranking, song, artists, reproductions, album, duration in allData], file, indent = 4, ensure_ascii=False)

print("Data saved on Json")