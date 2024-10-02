from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
from database import database 

option=Options()
option.add_experimental_option("detach",True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=option)
driver.get("https://ppubs.uspto.gov/pubwebapp/static/pages/ppubsbasic.html")
driver.maximize_window()



search_term1 = "ai"
search_term2 = "agriculture"
# Locate the search box element (replace with actual HTML element identifiers)

search_box1 = driver.find_element(By.ID, "searchText1")  # Replace with actual ID
search_box2 = driver.find_element(By.ID, "searchText2") 
# Send the search term to the search box
search_box1.send_keys(search_term1)
search_box2.send_keys(search_term2)




button = driver.find_element(By.ID, "basicSearchBtn") 

for _ in range(10):  # Adjust the number of attempts as needed
    try:
        # Wait for the tag to appear
        button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "even")))  # Replace with actual tag name
        break  # If the tag is found, break the loop
        
    except:
        try:
          buttonOK = driver.find_element(By.CLASS_NAME,"QSIWebResponsiveDialog-Layout1-SI_7WgrKZZwMjtuFh4_button QSIWebResponsiveDialog-Layout1-SI_7WgrKZZwMjtuFh4_button-medium QSIWebResponsiveDialog-Layout1-SI_7WgrKZZwMjtuFh4_button-border-radius-slightly-rounded")
        except:# If the tag is not found, click the button and wait for 30 seconds
           time.sleep(10)

