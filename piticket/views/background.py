import pygame 
from piticket.videoplayer import VideoPygame
from piticket.utils import multiline_text_to_surfaces
from piticket.pictures import get_filename
from piticket.views.box import Box, Header, Footer, RightSideBar, LeftSideBar, Button
from piticket.views.row import RowView


class Background():
    def __init__(self, image_name, 
                bg_color=(255,255,255), 
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

        self._header = Header(parent=surface, height=160, 
                            color=(0, 106, 78), border_color=(0, 106, 78),
                            padding=0, margin=25,
                            content=get_filename('nrc.jpg'), 
                            content_position='top-right')
        self._left_sidebar = LeftSideBar(parent=surface, width=160, 
                            margin=25, color=(208, 240, 192), 
                            border_color=(208, 240, 192))

        self._footer = None
        self._right_sidebar = None

        self._need_update = None

        self.event = None

    def __str__(self):
        return "{}-{}".format(self._name, self.__class__.__name__)

    def handle_events(self, event=None):
        if not event:
            return 
        if event:
            self.event = event

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

    def get_color(self):
        """Get background color (RGB tuple)"""
        return self._bg_color

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
            self._need_update = True

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
    def __init__(self, path, surface):
        Background.__init__(self, path, surface=surface)
        self.video = VideoPygame(self._name)

    def paint(self, screen):
        self.video.preview(screen)

class ChooseBackground(Background):
    def __init__(self, surface):
        Background.__init__(self, 'choose', surface=surface)
        # position of title and options
        x = self._left_sidebar.width + self._left_sidebar.margin
        y = self._header.height + self._header.margin
        width = surface.get_rect().width-2*self._left_sidebar.width-self._left_sidebar.margin
        self.title = Box(parent=surface,
                        x=x, y=y, width=width,
                        height=60, padding=10,
                        margin=0,
                        border=0,
                        border_radius=0,
                        border_color=None, 
                        content='Welcome, touch screen to continue',
                        content_color=(0,0,0),
                        content_position='center',
                        color=self.get_color(),
                        position=None,
                        interactable=False)
        # change y for buttons
        y = y+self.title.height
        self.options = Box(parent=surface,
                        x=x, y=y, width=width,
                        height=160, padding=10,
                        margin=20,
                        border=0,
                        border_radius=0,
                        border_color=None, 
                        content=None,
                        content_color=None,
                        content_position=None,
                        color=self.get_color(),
                        position=None,
                        interactable=False)
        # Add all these buttons to options attribute
        self.recharge_card = Button(parent=self.options, 
                        x=0, y=0, width=240, 
                        height=160, padding=0,
                        content=get_filename('mastercard.png'),
                        content_position='center',
                        position='top-left')
        self.all_travels = Button(parent=self.options, 
                        x=0, y=0, width=240, 
                        height=160, padding=0,
                        content=get_filename('mastercard.png'),
                        content_position='center',
                        position='center')
        self.collect_ticket = Button(parent=self.options, 
                        x=0, y=0, width=240, 
                        height=160, padding=0,
                        content=get_filename('mastercard.png'),
                        content_position='center',
                        position='top-right') 
        
        # Add title below the buttons
        x = x
        y = y + self.options.rect.height + self.options.margin
        self.second_title = Box(parent=surface,
                        x=x, y=y, width=width,
                        height=50, padding=10,
                        margin=0,
                        border=0,
                        border_radius=0,
                        border_color=None, 
                        content='Quick ticket selections for popular destinations',
                        content_color=(0,0,0),
                        content_position='center',
                        color=self.get_color(),
                        position=None,
                        interactable=False)
        # This box holds two views with the content dynamically generated
        height=surface.get_rect().height - (self._header.height + self.title.height + self.options.height + self.second_title.height + 50)
        
        self.travel_box_options = Box(parent=surface,
                        x=x, y=y+self.second_title.height, width=width,
                        height=height, padding=10,
                        margin=0,
                        border=2,
                        border_radius=0,
                        border_color=(0,0,0), 
                        content=None,
                        content_color=(0,0,0),
                        content_position='center',
                        color=self.get_color(),
                        position=None,
                        interactable=False)
        # print('travel_box_height', self.travel_box_options.height)
        # print('travel_box_width', self.travel_box_options.width)
        # print('screen height: ', surface.get_rect().height)
        # exit()
        # split options into two views under travel box options
        # height = height - 5*self.travel_box_options.padding
        
        self.left_options = RowView(parent=self.travel_box_options,
                        x=0, y=0, width=width//2,
                        height=height, padding=20,
                        margin=30,
                        border=2,
                        border_radius=0,
                        border_color=self.get_color(), 
                        content=None,
                        content_color=self._header.get_color(),
                        content_position='top-left',
                        color=self.get_color(),
                        position='top-left',
                        interactable=False)
        self.right_options = RowView(parent=self.travel_box_options,
                        x=0, y=0, width=width//2,
                        height=height, padding=20,
                        margin=30,
                        border=2,
                        border_radius=0,
                        border_color=self.get_color(), 
                        content=None,
                        content_color=self._header.get_color(),
                        content_position='top-right',
                        color=self.get_color(),
                        position='top-right',
                        interactable=False)

        # print('left_options_height', self.left_options.height)
        # print('left_options_width', self.left_options.width)
        # print('right_options_height', self.right_options.height)
        # print('right_options_width', self.right_options.width)

    def paint(self,screen):
        Background.paint(self,screen)
        if self.title:
            self.title.draw(screen)
        if self.recharge_card:
            self.recharge_card.update(self.event, screen)
        if self.all_travels:
            self.all_travels.update(self.event, screen)
        if self.collect_ticket:
            self.collect_ticket.update(self.event, screen)
        if self.second_title:
            self.second_title.draw(screen)
        if self.travel_box_options:
            self.travel_box_options.draw(screen)
        if self.left_options:
            self.left_options.update(self.event,screen)
        if self.right_options:
            self.right_options.update(self.event,screen)
        
        
class ChosenBackground(Background):
    def __init__(self, surface):
        Background.__init__(self, 'chosen', surface=surface)