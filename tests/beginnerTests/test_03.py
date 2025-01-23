# This test is to verify the use of cookies for load the page already logged
import pickle
from selenium import webdriver
# This line is necesary for search the HTML elements
from selenium.webdriver.common.by import By
# Libraries for implicit waits
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# load driver
driver = webdriver.Chrome()

# Open Spotify
driver.get("https://open.spotify.com/")
# Wait for  elements to load
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

# close browser
driver.quit()