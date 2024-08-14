import pygame
import os
import os.path as osp
from PIL import Image, ImageOps

from piticket.utils import rename_gifs
from piticket.pictures.sizing import new_size_keep_aspect_ratio, new_size_by_croping_ratio

def get_filename(name):
    """Return absolute path to a picture located in the current package.

    :param name: name of an image located in pitcures/assets
    :type name: str

    :return: absolute image path
    :rtype: str
    """
    return osp.join(osp.dirname(osp.abspath(__file__)), 'assets', name)

def get_gifs(name):
    """Each gif has been split into frames under a directory assets/gifs.
    Given the name of the directory, retrieve a list of the full path of all
    the frames.
    :param name: the name of the gif
    :type name: str
    """
    _dir = osp.join(get_filename('gifs'),name)
    frames = os.listdir(_dir)
    fullpath_frames = []
    for frame in frames:
        fullpath_frames.append(osp.join(_dir,frame))
    return sorted(fullpath_frames)

def colorize_pil_image(pil_image,color,bg_color=None):
    if not bg_color:
        bg_color = (abs(color[0] - 255), abs(color[1] - 255), abs(color[2] - 255))
    _, _, _, alpha = pil_image.split()
    gray_pil_image = pil_image.convert('L')
    new_pil_image = ImageOps.colorize(gray_pil_image, black=bg_color, white=color)
    new_pil_image.putalpha(alpha)
    return new_pil_image

def get_pygame_image(name, size=None, antialiasing=True, hflip=False, vflip=False, 
                    crop=False, angle=0, color=(255,255,255), bg_color=None):
    """Return a pygame image. If a size is given, the image is resized
     and the aspect ratio is preserved.
    
    :param name: name of an image to be turned into pygame surface
    :type name: str
    :param size: 
    :type size: tuple
    :param antialiasing: use antialiasing algorithm when resizing image
    :type antialiasing: bool
    :param hflip: apply horizontal flip
    :type hflip: bool
    :param crop: crop image to fit aspect ratio of the size
    :type crop: bool
    :param angle: angle of rotation of the image
    :type angle: int
    :param color: recolorize the image with this RGB color
    :type color: tuple
    :param bg_color: recolorize the image background with this color
    :type bg_color: tuple

    :return: pygame.Surface with image
    :rtype: object
    """
    if not name.startswith('/home/'):
        path = name
    else:
        path = get_filename(name)
    if not size and not color:
        image = pygame.image.load(name).convert()
    else:
        if osp.isfile(path):
            pil_image = Image.open(path).convert('RGBA')
        else:
            pil_image = Image.new('RGBA', size, (0,0,0,0))
        if color:
            pil_image = colorize_pil_image(pil_image, color, bg_color)
        if size:
            if crop:
                pil_image = pil_image.crop(new_size_by_croping_ratio(pil_image.size,size))
            pil_image = pil_image.resize(new_size_keep_aspect_ratio(pil_image.size, size), Image.LANCZOS if antialiasing else Image.NEAREST)

        image = pygame.image.frombuffer(pil_image.tobytes(), pil_image.size, pil_image.mode)

    if hflip or vflip:
        image = pygame.transform.flip(image, hflip, vflip)
    if angle != 0:
        image = pygame.transform.rotate(image, angle)
    return image