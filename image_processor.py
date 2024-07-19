from io import BytesIO
import requests
from PIL import Image
from rembg import remove


def remove_white_background(img):
    return remove(Image.open(img))


def load_image_from_url(url):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    img = BytesIO(response.raw.read())

    return img

class ImageProcessor:
    
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        pass
    
    def remove_backround(self, img_url):
        return remove_white_background(load_image_from_url(img_url))
