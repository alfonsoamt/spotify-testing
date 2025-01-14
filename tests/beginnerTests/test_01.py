from selenium import webdriver

# Load the driver for Chrome
driver = webdriver.Chrome()

# Open Spotify
driver.get("https://open.spotify.com/")

# Print page contents
print(driver.title)
print(driver.current_url)

# Close browser
driver.quit()