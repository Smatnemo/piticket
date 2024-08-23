import pygame 
from piticket.videoplayer import VideoPygame
from piticket.utils import multiline_text_to_surfaces
from piticket.pictures import get_filename
from piticket.language import get_translated_text
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
         # position of title and options
        x = self._left_sidebar.width + self._left_sidebar.margin
        y = self._header.height + self._header.margin
        width = surface.get_rect().width-2*self._left_sidebar.width-self._left_sidebar.margin
        self.title = Box(parent=surface, x=x, y=y, width=width,
                                height=60, padding=10, margin=0, border=0,
                                border_radius=0, border_color=None, content=get_translated_text(self._name),
                                content_color=(0,0,0), content_position='center', color=self.get_color(),
                                position=None, interactable=False)
        self.side_bar_top = Box(parent=self._left_sidebar,
                                x=0, y=160, width=self._left_sidebar.width,
                                height=160, padding=10, margin=20,
                                border=0, border_radius=0,
                                border_color=(255,255,0), content=None,
                                content_color=None, content_position=None,
                                color=self._left_sidebar.get_color(),
                                position=None, interactable=False)
        self.side_bar_center = Box(parent=self._left_sidebar,
                                x=0, y=160, width=self._left_sidebar.width,
                                height=240, padding=10, margin=20,
                                border=0, border_radius=0,
                                border_color=(255,255,0), content=None,
                                content_color=None, content_position=None,
                                color=self._left_sidebar.get_color(),
                                position=Box.CENTER, interactable=False)
        self.side_bar_bottom = Box(parent=self._left_sidebar,
                                x=0, y=0, width=self._left_sidebar.width,
                                height=160, padding=10, margin=20,
                                border=0, border_radius=0,
                                border_color=(255,255,0), content=None,
                                content_color=None, content_position=None,
                                color=self._left_sidebar.get_color(),
                                position=Box.BOTTOMLEFT,
                                interactable=False)

        self._footer = None
        self._right_sidebar = None

        self._need_update = None

        self.event = None

    def __str__(self):
        return "{}-{}".format(self._name, self.__class__.__name__)

    def handle_events(self, event=None):
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
        if self.side_bar_top:
            self.side_bar_top.draw(screen)
        if self.side_bar_center:
            self.side_bar_center.draw(screen)
        if self.side_bar_bottom:
            self.side_bar_bottom.draw(screen)
        if self._footer:
            self._footer.draw(screen)
        if self._header:
            self._header.draw(screen)
        if self.title:
            self.title.draw(screen)


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
    def __init__(self, tickets, surface):
        Background.__init__(self, 'choose', surface=surface)
        
        x = self._left_sidebar.width + self._left_sidebar.margin
        y = self.title.y+self.title.height
        self.options = Box(parent=surface,
                        x=x, y=y, width=self.title.width,
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
                        height=160, padding=0, border=0,
                        content=get_filename('mastercard.png'),
                        content_position='center',
                        color=self.get_color(),
                        position='top-left')
        self.all_travels = Button(parent=self.options, 
                        x=0, y=0, width=240, 
                        height=160, padding=0, border=0,
                        content=get_filename('mastercard.png'),
                        content_position='center',
                        color=self.get_color(),
                        position='center')
        self.collect_ticket = Button(parent=self.options, 
                        x=0, y=0, width=240, 
                        height=160, padding=0, border=0,
                        content=get_filename('mastercard.png'),
                        content_position='center',
                        color=self.get_color(),
                        position='top-right') 
        
        # Add title below the buttons
        x = x
        y = y + self.options.rect.height + self.options.margin
        self.second_title = Box(parent=surface,
                        x=x, y=y, width=self.title.width,
                        height=50, padding=10,
                        margin=0,
                        border=0,
                        border_radius=0,
                        border_color=None, 
                        content=get_translated_text('quick'),
                        content_color=(0,0,0),
                        content_position='center',
                        color=self.get_color(),
                        position=None,
                        interactable=False)

        # This box holds two views with the content dynamically generated
        height=surface.get_rect().height - (self._header.height + self.title.height + self.options.height + self.second_title.height + 50)
        self.travel_box_options = Box(parent=surface,
                        x=x, y=y+self.second_title.height, width=self.title.width,
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
        # split options into two views under travel box options
        # height = height - 5*self.travel_box_options.padding
        self.left_options = RowView(parent=self.travel_box_options,
                        x=0, y=0, width=self.title.width//2,
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
                        interactable=False,
                        rows=tickets)
        self.right_options = RowView(parent=self.travel_box_options,
                        x=0, y=0, width=self.title.width//2,
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
                        interactable=False,
                        rows=tickets)
        # Create options for the side bar
        # Show that card payment is available
        self.card_text = Box(parent=self.side_bar_top,
                        x=0, y=0, width=120,
                        height=40, padding=0,
                        margin=0,
                        border=0,
                        border_radius=0,
                        border_color=None, 
                        content=get_translated_text('card'),
                        content_color=(0,0,0),
                        content_position='center',
                        color=self.side_bar_top.get_color(),
                        position=Box.TOPCENTER,
                        interactable=False)
        self.card_payment = Box(parent=self.side_bar_top,
                        x=0, y=0, width=150,
                        height=100, padding=0,
                        margin=0,
                        border=0,
                        border_radius=0,
                        border_color=None, 
                        content=get_filename('mastercard.png'),
                        content_color=(0,0,0),
                        content_position='center',
                        color=self.side_bar_top.get_color(),
                        position=Box.CENTER,
                        interactable=False)
        self.translations = Button(parent=self.side_bar_center, 
                        x=0, y=0, width=150, 
                        height=100, padding=0, border=0,
                        content=get_filename('mastercard.png'),
                        content_position='center',
                        color=self.side_bar_center.get_color(),
                        position=Box.CENTER)

        self.future_tickets = Button(parent=self.side_bar_bottom, 
                        x=0, y=0, width=150, 
                        height=100, padding=20, border=0,
                        content=get_translated_text('future'),
                        content_position='center',
                        color=self._header.get_color(),
                        position=Box.TOPCENTER)

    def paint(self,screen):
        Background.paint(self,screen)
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
        if self.card_text:
            self.card_text.draw(screen)
        if self.card_payment:
            self.card_payment.draw(screen)
        if self.translations:
            self.translations.update(self.event, screen)
        if self.future_tickets:
            self.future_tickets.update(self.event, screen)
        
        
class ChosenBackground(Background):
    def __init__(self, chosen_ticket, surface):
        Background.__init__(self, 'chosen', surface=surface)
        self.chosen_ticket = chosen_ticket
        self.back_button = Button(parent=self.side_bar_bottom, 
                        x=0, y=0, width=120, 
                        height=60, padding=20,
                        content='Back',
                        content_position='center',
                        color=self._header.get_color(),
                        position='top-center')
        self.back_button.clicked(pygame.event.post, (pygame.event.Event(pygame.MOUSEBUTTONUP,state='choose')))
        self.cancel_button = Button(parent=self.side_bar_bottom, 
                        x=0, y=0, width=120, 
                        height=60, padding=20,
                        content='Cancel',
                        content_position='center',
                        color=(255,0,0),
                        position='bottom-center')
        self.cancel_button.clicked(pygame.event.post, (pygame.event.Event(pygame.MOUSEBUTTONUP,state='wait')))
        
    def paint(self, screen):
        Background.paint(self, screen)
        if self.cancel_button:
            self.cancel_button.update(self.event, screen)
        if self.back_button:
            self.back_button.update(self.event, screen)