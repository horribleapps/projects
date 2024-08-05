import time
from selenium import webdriver
from urllib.parse import unquote 
from selenium.webdriver.common.by import By
import pdb
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


'''driver.get('http://www.google.com/');
time.sleep(5) # Let the user actually see something!
search_box = driver.find_element("name","q")
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5) # Let the user actually see something!
driver.quit()'''

def search(query):
    #DRIVER_PATH = '/usr/bin/firefox'
    cservice = webdriver.ChromeService(executable_path='/usr/bin/chromedriver')
    driver   = webdriver.Chrome(service=cservice)  # Optional argument, if not specified will search path.
    
    #query="15mL conical"

    # For one word queries it will be ok, for complex ones should encode first
    driver.get(f'https://duckduckgo.com/?q={query}&t=h_&iax=images&ia=images') 
    pdb.set_trace()
    # For now it's working with this class, not sure if it will never change
    #img_tags = driver.find_element(By.CLASS_NAME,'tile  tile--img')
    tag1 = driver.find_element(By.CLASS_NAME,'body--serp ')
    tag1 = driver.find_element(By.CLASS_NAME,'zci__main  zci__main--tiles  js-tiles   has-nav tileview__images has-tiles--grid')
    #tag2 = 
    print(tag1)
    '''for tag in img_tags:
        src = tag.get_attribute('data-src')
        src = unquote(src)
        src = src.split('=', maxsplit=1)
        src = src[1]
        yield src'''

    driver.close()

if __name__ == '__main__':
    from pprint import pprint
    imgs_urls = list(search('15mL conical'))
    pprint(imgs_urls)
