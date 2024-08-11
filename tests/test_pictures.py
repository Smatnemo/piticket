import os.path as osp
from PIL import Image
from piticket.pictures import get_filename, get_pygame_image
from piticket.pictures.sizing import (new_size_keep_aspect_ratio, 
                                    new_size_by_croping_ratio, new_size_by_croping)

name = 'pibooth.png'
full_name = osp.join('/home/pi/Dev/piticket/piticket/pictures/assets',name)
image = Image.open(full_name)

def test_get_filename():
    assert full_name == get_filename(name)

def test_new_size_keep_aspect_ratio():
    new_size_keep_aspect_ratio(image.size, (100, 100))

def test_new_size_by_croping_ratio():
    print(new_size_by_croping_ratio(image.size, (100, 100)))

def test_new_size_by_croping():
    new_size_by_croping(image.size,(100,100))

def test_get_pygame_image():
    get_pygame_image(name, (100,100))