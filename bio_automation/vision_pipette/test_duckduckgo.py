from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from os import path, makedirs
import requests
import uuid
import ast

search_string = "15mL centrifuge tubes"  # Search string
download_folder = "downloads/15mL_centrifuge_tube"  # Where to download images to
min_amount = 1  # Download at least this many images

cservice = ChromeService(executable_path='/usr/bin/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run headless Chrome
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

wd = webdriver.Chrome(service=cservice, options=options)

wd.get("https://images.bing.com")
search_box = wd.find_element(By.ID, "sb_form_q")
search_box.send_keys(search_string + Keys.ENTER)
time.sleep(3)  # wait to load

def download_image(url, headers, folder, filename_counter):
    try:
        img_path = path.join(folder, f"img_{str(uuid.uuid1())[0:15]}.jpg")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        with open(img_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {url}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Skipped: {url}, error: {e}")
        return False

def download_images(thumbnails, folder, filename_counter):
    makedirs(folder, exist_ok=True)  # create directory to save images
    delay_time = 5  # reduce delay to 5 seconds for testing
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://images.bing.com'
    }
    for pic in thumbnails:
        try:
            strOI = pic.get_attribute("m")
            dct = ast.literal_eval(strOI)
            url = dct['murl']
            print(f"Attempting to download: {url}")
            success = download_image(url, headers, folder, filename_counter)
            if success:
                filename_counter += 1
            time.sleep(delay_time)
        except Exception as e:
            print(f"Error processing thumbnail: {e}")
            #filename_counter += 1
            time.sleep(delay_time)
        if filename_counter>20:
	        break
    return filename_counter

def scroll_to_end(wd):
    """Function to scroll down after saving all images in window"""
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)  # allow loading before continuing

file_counter = 0
while file_counter < min_amount:
    thumbnails = wd.find_elements(By.CLASS_NAME, "iusc")
    file_counter = download_images(thumbnails, folder=download_folder, filename_counter=file_counter)
    scroll_to_end(wd)

wd.quit()
