from jmd_imagescraper.core import * # dont't worry, it's designed to work with import *
from pathlib import Path

root = Path().cwd()/"images"

duckduckgo_search(root, "Cats", "cute kittens", max_results=20)



#from jmd_imagescraper.imagecleaner import *

#display_image_cleaner(root)
