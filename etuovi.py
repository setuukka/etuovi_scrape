#Tämä ohjelma hakee kaikkien myynnissä olevien Oulun kerrostaloasuntojen tiedot
#Ja tallentaa ne päivämäärä_listings.csv nimettyyn tiedostoon.
#Se avataan käsittelyä varten soup_testing.py tiedostossa

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import time
import random
from datetime import datetime

service = Service('chromedriver.exe')

chrome_options = Options()
#chrome_options.add_argument('--headless')  # Run in headless mode
chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration (required for headless mode on Windows)
chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
driver = webdriver.Chrome(service=service, options = chrome_options)

def wait_random():
    wait_time = random.uniform(1, 3)
    print(f"Waiting for {wait_time:.2f} seconds")
    time.sleep(wait_time)

#url = 'https://www.etuovi.com/haku/myytavat-asunnot'
#url = 'https://www.etuovi.com/myytavat-asunnot/oulu?haku=M2134060496' #kerrostalot
url = 'https://www.etuovi.com/myytavat-asunnot/oulu?haku=M2140784029' #kaikki
print(url)
driver.get(url)
driver.implicitly_wait(10)

# #Jos tulee cookies-popup
try:
    accept_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "almacmp-modalConfirmBtn"))
    )
    accept_button.click()
except Exception as e:
    print(f"An error occurred: {e}")

#Accessing <a hrefs>
print("first page")
url_list = []
a_tags = driver.find_elements(By.TAG_NAME, 'a')

filtered_hrefs = [a.get_attribute('href') for a in a_tags 
                  if a.get_attribute('href') is not None and "kohde" in a.get_attribute('href')]
for href in filtered_hrefs:
    filtered_href = href.split('?')[0]
    url_list.append(filtered_href) 


#haetaan muut sivut
while True:
    try:
        wait_random()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        #Tallennetaan linkit
        a_tags = driver.find_elements(By.TAG_NAME, 'a')

        filtered_hrefs = [a.get_attribute('href') for a in a_tags 
                        if a.get_attribute('href') is not None and "kohde" in a.get_attribute('href')]
        for href in filtered_hrefs:
            filtered_href = href.split('?')[0]
            url_list.append(filtered_href)
        url_list += filtered_hrefs
        print(len(url_list))
        #valitaan seuraava sivu-nappi
        wait_random()
        next_page_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button#paginationNext[title="Seuraava sivu"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", next_page_button)
        next_page_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        time.sleep(0.2)
        print("Working...")

    except Exception as e:
        # If there is an exception (e.g., "Next Page" button not found), break the loop
        print(f"An exception occurred: {e}")
        break

driver.quit()


current_date = datetime.now().strftime('%d%m%Y')

filename = f"{current_date}_listings.csv"
df = pd.DataFrame(url_list, columns=['URL'])
#Siivotaan vähän df:ää

df['URL'] = df['URL'].str.split('?').str.get(0)
df = df.drop_duplicates()

print("Writing to csv")
df.to_csv(filename, index=False)
print("Save complete!")

