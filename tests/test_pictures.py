import os.path as osp
from piticket.pictures import get_filename

name = 'camera.png'
full_name = osp.join('/home/pi/Dev/piticket/piticket/pictures/assets',name)

def test_get_filename():
    assert full_name == get_filename(name)