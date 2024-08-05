import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

    search_url = f"https://www.google.com/search?q={query}&tbm=isch"

    print(f"Fetching URL: {search_url}")
    wd.get(search_url)

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        thumbnail_results = wd.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")
        number_results = len(thumbnail_results)
        print(f"Found thumbnails: {number_results}")

        for img in thumbnail_results[results_start:number_results]:
            try:
                wd.execute_script("arguments[0].scrollIntoView();", img)
                WebDriverWait(wd, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img.Q4LuWd")))
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception as e:
                print(f"Could not click on thumbnail - {e}")
                continue

            actual_images = wd.find_elements(By.CSS_SELECTOR, 'img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
        else:
            results_start = len(thumbnail_results)

    return image_urls

def download_images(folder_path: str, urls: set):
    for i, url in enumerate(urls):
        try:
            print(f"Downloading {url}")
            image_content = requests.get(url).content
        except Exception as e:
            print(f"ERROR - Could not download {url} - {e}")
            continue
F
        try:
            with open(os.path.join(folder_path, f"jpg_{i}.jpg"), 'wb') as f:
                f.write(image_content)
        except Exception as e:
            print(f"ERROR - Could not save {url} - {e}")
            continue

if __name__ == "__main__":
    DRIVER_PATH = '/usr/bin/chromedriver'  # Path to your Chromium driver
    options = webdriver.ChromeOptions()
    options.binary_location = '/usr/bin/chromium-browser'  # Path to your Chromium browser
    options.add_argument('--headless')  # Run in headless mode (optional)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    try:
        wd = webdriver.Chrome(service=Service(DRIVER_PATH), options=options)
    except Exception as e:
        print(f"ERROR - Could not start the WebDriver - {e}")
        exit()

    query = "15mL centrifuge tube"
    max_links_to_fetch = 100
    try:
        urls = fetch_image_urls(query, max_links_to_fetch, wd)
    except Exception as e:
        print(f"ERROR - Problem during fetching images - {e}")
    finally:
        wd.quit()

    print(f"Found {len(urls)} URLs")
    os.makedirs('images', exist_ok=True)
    download_images('images', urls)
