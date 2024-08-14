import pygame 
from piticket.fonts import get_pygame_font
from piticket.videoplayer import VideoPygame

def multiline_text_to_surfaces(text, color, rect, align='center'):
    """Return a list of text surfaces(pygame.Surface) and corresponding positions
    The ``align```parameter can be one of:
        * top-left
        * top-center
        * top-right
        * center-left
        * center
        * center-right
        * bottom-left
        * bottom-center
        * bottom-right
    """
    surfaces = []
    # split text into list of strings using newline character
    lines = text.splitlines()
    # Return a SysFont object corresponding to the longest string
    font = get_pygame_font(max(lines, key=len),'nimbussansnarrow',rect.width,rect.height//len(lines))

    for i, line in enumerate(lines):
        surface = font.render(line, True, color)
        if align.endswith('left'):
            x = rect.left
        elif align.endswith('center'):
            x = rect.centerx - surface.get_rect().width//2
        elif align.endswith('right'):
            x = rect.right - surface.get_rect().width
        else:
            raise ValueError("Invalid horizontal argument '{}'".format(align))

        height = surface.get_rect().height
        if align.startswith('top'):
            y = rect.top + i*height
        elif align.startswith('center'):
            y = rect.centery - (len(lines)*height)//2 + height*i
        elif align.startswith('bottom'):
            y = rect.bottom - len(lines)*height + i*height
        else:
            raise ValueError("Invalid vertical argument '{}'".format(align))
   
        surfaces.append((surface,surface.get_rect(x=x,y=y)))

    return surfaces

class Background():
    def __init__(self, image_name, 
                bg_color=(0,0,0), 
                text_color=(255,255,255), 
                font_size=12):
        """
        :attr _bg_color: background color
        :type _bg_color: tuple
        :attr _text_color: text color
        :type _text_color: tuple
        :attr _name: name of the background text to be written
        :type _name: string
        :attr _rect: the rectangle of the window
        :type _rect: pygame.Rect
        :attr font: is a font object used to render text to pygame surface
        :type font: pygame.font.SysFont or pygame.font.Font

        """
        self._bg_color = bg_color 
        
        self._name = image_name

        self._texts = []
        self._text_border = 20 # Distance to other elements
        self._text_color = text_color

        self.font = None
        self.font_size = font_size

        self._rect = None

        self._popup_box = None

        self._need_update = None

    def __str__(self):
        return "{}-{}".format(self._name, self.__class__.__name__)

    def handle_events(self, events=[]):
        pass 

    def _write_texts(self, text, rect=None):
        """Create text surfaces to draw on window surface.
        :param text: text to be written on screen
        :type param: str
        :param rect: the rect determines the 
        """
        if not rect:
            # Reduce the size of the screen's rect by self._text_border
            rect = self._rect.inflate(-self._text_border, -self._text_border)
        
        if rect.height != self.font_size:
            self.font_size = rect.height

        self._texts.extend(multiline_text_to_surfaces(text, self._text_color,rect))

    def set_color(self, color_or_path):
        """Set background color using RGB tuple or path to an image
        
        :param color_or_path: RGB color tuple or image path
        :type color_or_path: tuple or str
        """
        assert len(color_or_path) == 3, "Length of 3 is required (RGB tuple)"
        self._bg_color = color_or_path

    def set_text_color(self, color):
        """"""
        assert len(color) == 3, "Length of 3 is required (RGB tuple)"
        self._text_color = color

    def resize_texts(self, rect=None):
        """Resize text pygame surfaces"""
        self._write_texts('Ticket text\nNext Please step forward!', rect)

    def resize(self, screen):
        """Resize objects to fit to the screen
        """
        if self._rect != screen.get_rect():
            self._rect = screen.get_rect()

        self.resize_texts()

    def paint(self, screen):
        screen.fill(self._bg_color)
        for text_surface, pos in self._texts: 
            screen.blit(text_surface, pos)
        


class VideoBackground(Background):
    def __init__(self, path):
        Background.__init__(self, path)
        self.video = VideoPygame(self._name)
        self.video.play()

    def resize(self, screen):
        pass

    def paint(self, screen):
        self.video.preview(screen)


class IntroBackground(Background):
    def __init__(self):
        Background.__init__(self, 'intro') 