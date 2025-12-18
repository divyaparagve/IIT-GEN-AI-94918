from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
driver = webdriver.Chrome() # 1. Start the Session - Selenium Manager handles driver
driver.get("https://duckduckgo.com/") # 2. Take Action on Browser
print("Page title is:", driver.title) # 3. Request Browser Information
driver.implicitly_wait(10) # 4. Wait strategy: Wait up to 5 seconds for elements to appear
search_box = driver.find_element(By.NAME, "q") # 5. Find element search box by its name
# 6. Take Action on Element
search_box.clear() # Clear any pre-filled text
search_box.send_keys("Python for beginners") # Type the query
search_box.send_keys(Keys.RETURN) # Press Enter
driver.implicitly_wait(5)
print("New page title is:", driver.title) # 7. Request Element Information
time.sleep(10)
# Optional: Wait a moment to see the result time.sleep(10)
driver.quit() # 8. End the Session