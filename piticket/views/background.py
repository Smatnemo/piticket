import pygame 
from piticket.videoplayer import VideoPygame
from piticket.utils import multiline_text_to_surfaces
from piticket.views.box import Header, Footer, RightSideBar, LeftSideBar


class Background():
    def __init__(self, image_name, 
                bg_color=(0,0,0), 
                text_color=(255,255,255), 
                font_size=12,
                surface=None):
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
        :attr surface: pygame surface to initialize header, footer and left and right sidebars
        :thype surface: pygame.Surface
        """
        self._bg_color = bg_color 
        
        self._name = image_name

        self._texts = []
        self._text_border = 20 # Distance to other elements
        self._text_color = text_color

        self.font = None
        self.font_size = font_size

        self._rect = None

        self._header = None
        self._footer = None
        self._left_sidebar = None
        self._right_sidebar = None
        self._popup_box = None

        self._need_update = None

    def __str__(self):
        return "{}-{}".format(self._name, self.__class__.__name__)

    def handle_events(self, event=None):
        if not event:
            return 
        if event:
            self._need_update = event

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
        self._texts = []
        text = 'Ticket'
        if text:
            self._write_texts(text, rect)

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
        if self._right_sidebar:
            self._right_sidebar.draw(screen)
        if self._left_sidebar:
            self._left_sidebar.draw(screen)
        if self._footer:
            self._footer.draw(screen)
        if self._header:
            self._header.draw(screen)


class IntroBackground(Background):
    def __init__(self, surface):
        Background.__init__(self, 'intro', surface=surface)

class VideoBackground(Background):
    def __init__(self, path):
        Background.__init__(self, path)
        self.video = VideoPygame(self._name)

    def paint(self, screen):
        self.video.preview(screen)

class ChooseBackground(Background):
    def __init__(self, surface):
        Background.__init__(self, 'choose', surface=surface) 
        self._header = Header(parent=surface, color=(0, 73, 83), border_color=(0, 73, 83))
        self._left_sidebar = LeftSideBar(parent=surface, color=(208, 240, 192), border_color=(208, 240, 192))
        
        
class ChosenBackground(Background):
    def __init__(self, surface):
        Background.__init__(self, 'chosen', surface=surface)