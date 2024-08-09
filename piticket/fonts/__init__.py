import pygame 

def get_available_fonts():
    """Return the list of available fonts"""
    sys_available_fonts = pygame.font.get_available_fonts()
    return sys_available_fonts 

def get_pygame_font(text, font_name, max_width, max_height):
    """Create the pygame font object which fit the text to the given rectangle.
    
    :param text: text to draw
    :type text: str
    :param font_name: name or path to font definition file
    :type font_name: str
    :param max_width: width of the rect to fit
    :type max_width: int
    :param max_height: height of the rect to fit
    :type max_height: int
    """
    start, end = 0, int(max_height * 2)
    while start < end:
        k = (start + end) // 2
        font = pygame.font.SysFont(font_name,k)
        font_size = font.size(text)
        if font_size[0] > max_width or font_size[1] > max_height:
            end = k 
        else:
            start = k + 1
        del font # Run garbage collector, to avoid opening too many files
    return pygame.font.SysFont(font_name, start)

CURRENT = 'nimbussansnarrow'