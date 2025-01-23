from selenium import webdriver
# This line is necesary for search the HTML elements
from selenium.webdriver.common.by import By
# Libraries for implicit waits
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Library for the sensible data
from dotenv import load_dotenv
# Import OS library
import os
# Import pickle library to help the cookies saving
import pickle

# Load env variables
load_dotenv()
# save login variables to use in script
username = os.getenv("LOGIN_USER")
password = os.getenv("LOGIN_PASSWORD")


# Load the driver for Chrome
driver = webdriver.Chrome()

# Implicity wait
driver.implicitly_wait(5)

# Open Spotify
driver.get("https://open.spotify.com/")


# search for the login button
preLoginButton = driver.find_element(By.CSS_SELECTOR, "[data-testid='login-button']")
preLoginButton.click()

# Wait for  elements to load
wait = WebDriverWait(driver, 10)

# Search the username input field
usernameInput = wait.until(EC.visibility_of_element_located((By.ID, "login-username")))
print(usernameInput.get_attribute("placeholder"))

# Search the password input field
passwordInput = wait.until(EC.visibility_of_element_located((By.ID, "login-password")))
print(passwordInput.get_attribute("placeholder"))

# Screenshot before input the data
driver.save_screenshot('../../screenshots/beginner/login_page.png')
# Send logig data
usernameInput.send_keys(username)
passwordInput.send_keys(password)
# Screenshot after input the data
driver.save_screenshot('../../screenshots/beginner/data_input.png')
# Click login button
loginButton = driver.find_element(By.ID, "login-button")
loginButton.click()

# Verify login was successful
try:
    profileIcon = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='user-widget-link']")))
    print("Login successful!")

    # Save the login coockies in a binary file
    with open('../../cookies/cookies.pkl', 'wb') as file:
        pickle.dump(driver.get_cookies(), file)
    print("cookies saved!")
except:
    print("Login failed")

# Screenshot after login
driver.save_screenshot('../../screenshots/beginner/after_login.png')

# Close browser
driver.quit()