import json
import pygame 
from pygame.event import Event, post
from piticket.videoplayer import VideoPygame
from piticket.utils import multiline_text_to_surfaces
from piticket.pictures import get_filename
from piticket.language import get_translated_text, get_supported_languages, get_current_lang, rearrange_supported_languages
from piticket.views.box import Box, Header, Footer, RightSideBar, LeftSideBar, Button, Field
from piticket.views.row import RowView


class Background():
    def __init__(self, image_name, 
                bg_color=(240, 240, 223), 
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
        self.back_button = Button(parent=self.side_bar_bottom, 
                                x=0, y=0, width=120, 
                                height=60, padding=20,
                                content=get_translated_text('back'),
                                content_position='center',
                                color=self._header.get_color(),
                                position='top-center')
        self.back_button.clicked(post, Event(pygame.MOUSEBUTTONUP,state='choose'))
        self.cancel_button = Button(parent=self.side_bar_bottom, 
                                x=0, y=0, width=120, 
                                height=60, padding=20,
                                content=get_translated_text('cancel'),
                                content_position='center',
                                color=(255,0,0),
                                position='bottom-center')
        self.cancel_button.clicked(post, Event(pygame.MOUSEBUTTONUP,state='wait'))

         # position of title and options
        x = self._left_sidebar.width + self._left_sidebar.margin
        y = self._header.height + self._header.margin
        width = surface.get_rect().width-self._left_sidebar.width
        self.main_content = Box(parent=surface,
                                x=0, y=0, width=width,
                                height=self._left_sidebar.height-160, padding=10, margin=20,
                                border=2, border_radius=0,
                                border_color=(255,255,0), content=None,
                                content_color=None, content_position=None,
                                color=self.get_color(),
                                position=Box.BOTTOMRIGHT,
                                interactable=False)
        self.title = Box(parent=self.main_content, x=x, y=y, width=width-self._left_sidebar.margin-self._left_sidebar.width,
                                height=60, padding=10, margin=0, border=0,
                                border_radius=0, border_color=None, content=get_translated_text(self._name),
                                content_color=(0,0,0), content_position='center', color=self.get_color(),
                                position=Box.TOPCENTER, interactable=False)

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
        """Set background color using RGB tuple
        
        :param color_or_path: RGB color tuple
        :type color_or_path: tuple or list
        """
        if isinstance(color_or_path,(list,tuple)):
            assert len(color_or_path) == 3, "Length of 3 is required (RGB tuple)"
            if self._bg_color != color_or_path:
                self._bg_color = color_or_path
                self._need_update = True

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
        if self.main_content:
            self.main_content.draw(screen)
        if self.title:
            self.title.draw(screen)
        if self.cancel_button:
            self.cancel_button.update(self.event, screen)
        if self.back_button:
            self.back_button.update(self.event, screen)


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
        # Make back and cancel buttons None
        self.back_button = None 
        self.cancel_button = None

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
                        x=0, y=0, width=230, 
                        height=140, padding=0, border_radius=10,
                        content=get_filename('mastercard.png'),
                        content_position='center',
                        color=self.get_color(),
                        position=Box.TOPLEFT)
        self.recharge_card.clicked(post, Event(pygame.MOUSEBUTTONUP,state='recharge'))
        self.all_travels = Button(parent=self.options, 
                        x=0, y=0, width=230, 
                        height=140, padding=20, margin=0,
                        border_radius=10,
                        content=get_translated_text('destinations'),
                        content_position='center',
                        color=self._header.get_color(),
                        position=Box.TOPCENTER)
        self.collect_ticket = Button(parent=self.options, 
                        x=0, y=0, width=230, 
                        height=140, padding=20, border_radius=10,
                        content=get_translated_text('collect'),
                        content_position='center',
                        color=self._header.get_color(),
                        position=Box.TOPRIGHT) 
        
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
        
        # Create button for changing between translations
        self.translations = Button(parent=self.side_bar_center, 
                        x=0, y=0, width=150, 
                        height=100, padding=0, border=0,
                        content=None,
                        content_position='center',
                        color=self._header.get_color(),
                        position=Box.CENTER)
        self.translations.clicked(post,Event(pygame.MOUSEBUTTONUP,state='translate'))
        # create boxes for each language
        self.flags = [Box(parent=self.translations,
                        x=0, y=0, width=63,
                        height=42, padding=2,
                        margin=0,
                        border=0,
                        border_radius=0,
                        border_color=None, 
                        content=get_filename(f'{lang}_flag.png'),
                        content_color=(0,0,0),
                        content_position='center',
                        color=self.side_bar_top.get_color(),
                        position=position,
                        interactable=False) if lang==get_current_lang() else Box(parent=self.translations,
                                                                        x=0, y=0, width=42,
                                                                        height=28, padding=2,
                                                                        margin=0,
                                                                        border=0,
                                                                        border_radius=0,
                                                                        border_color=None, 
                                                                        content=get_filename(f'{lang}_flag.png'),
                                                                        content_color=(0,0,0),
                                                                        content_position='center',
                                                                        color=self.side_bar_top.get_color(),
                                                                        position=position,
                                                                        interactable=False)for lang, position in zip(rearrange_supported_languages(),[Box.CENTERLEFT, Box.CENTER, Box.CENTERRIGHT])]

        # Create button to navigate the calender for future travels
        self.future_tickets = Button(parent=self.side_bar_bottom, 
                        x=0, y=0, width=150, 
                        height=100, padding=20, border=0,
                        content=get_translated_text('future'),
                        content_position='center',
                        color=self._header.get_color(),
                        position=Box.TOPCENTER)
        self.future_tickets.clicked(post,Event(pygame.MOUSEBUTTONUP,state='future_tickets'))

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
        for flag in self.flags:
            flag.draw(screen)
        if self.future_tickets:
            self.future_tickets.update(self.event, screen)
        
        
class ChosenBackground(Background):
    def __init__(self, chosen_ticket, surface):
        Background.__init__(self, 'chosen', surface=surface)
        self.chosen_ticket = chosen_ticket
        label_font = 40
        label_width = 200
        height = self.main_content.height//12
        self.departure_field = Field(parent=self.main_content,
                                    x=0,y=self.title.height,
                                    width=self.main_content.width,
                                    height=height,
                                    position=None,
                                    margin=0, padding=0,
                                    border=0, border_radius=0,
                                    border_color=(255,0,0), label='Departure station',
                                    content=chosen_ticket['departure_station'],
                                    content_position=Box.CENTERLEFT,label_size=(label_width,label_font),
                                    color=self.get_color(),
                                    button1_config={'color':(0, 106, 78),'content':'Change','position':Box.CENTER,'size':{'width':100,'height':40}})

        self.destination_field = Field(parent=self.main_content,
                                    x=0,y=self.departure_field.y+self.departure_field.height,
                                    width=self.main_content.width,
                                    height=height,
                                    position=None,
                                    margin=0, padding=0,
                                    border=0, border_radius=0,
                                    border_color=(255,0,0), label='Destination station',
                                    content=chosen_ticket['destination'],
                                    content_position=Box.CENTERLEFT,label_size=(label_width,label_font),
                                    color=self.get_color(),
                                    button1_config={'color':(0, 106, 78),'content':'Change','position':Box.CENTER,'size':{'width':100,'height':40}})

        self.date_field = Field(parent=self.main_content,
                                    x=0,y=self.destination_field.y+self.destination_field.height,
                                    width=self.main_content.width,
                                    height=height,
                                    position=None,
                                    margin=0, padding=0,
                                    border=0, border_radius=0,
                                    border_color=(255,0,0), label='Date of travel',
                                    content=chosen_ticket['date_of_travel'],
                                    content_position=Box.CENTERLEFT,label_size=(label_width,label_font),
                                    color=self.get_color(),
                                    button1_config={'color':(0, 106, 78),'content':'Change','position':Box.CENTER,'size':{'width':100,'height':40}})

        self.route_field = Field(parent=self.main_content,
                                    x=0,y=self.date_field.y+self.date_field.height,
                                    width=self.main_content.width,
                                    height=height,
                                    position=None,
                                    margin=0, padding=0,
                                    border=0, border_radius=0,
                                    border_color=(255,0,0), label='Route',
                                    content=chosen_ticket['route'],
                                    content_position=Box.CENTERLEFT,label_size=(label_width,label_font),
                                    color=self.get_color())

        self.tickettype_field = Field(parent=self.main_content,
                                    x=0,y=self.route_field.y+self.route_field.height,
                                    width=self.main_content.width,
                                    height=height,
                                    position=None,
                                    margin=0, padding=0,
                                    border=0, border_radius=0,
                                    border_color=(255,0,0), label='Ticket type',
                                    content=chosen_ticket['ticket_type'],
                                    content_position=Box.CENTERLEFT,label_size=(label_width,label_font),
                                    color=self.get_color(),
                                    button1_config={'color':(0, 106, 78),'content':'Change','position':Box.CENTER,'size':{'width':100,'height':40}})

        self.railcard_field = Field(parent=self.main_content,
                                    x=0,y=self.tickettype_field.y+self.tickettype_field.height,
                                    width=self.main_content.width,
                                    height=height,
                                    position=None,
                                    margin=0, padding=0,
                                    border=0, border_radius=0,
                                    border_color=(255,0,0), label='Railcard',
                                    content=chosen_ticket['railcard'],
                                    content_position=Box.CENTERLEFT,label_size=(label_width,label_font),
                                    color=self.get_color(),
                                    button1_config={'color':(0, 106, 78),'content':'Change','position':Box.CENTER,'size':{'width':100,'height':40}})

        self.adults_field = Field(parent=self.main_content,
                                    x=0,y=self.railcard_field.y+self.railcard_field.height,
                                    width=self.main_content.width,
                                    height=height,
                                    position=None,
                                    margin=0, padding=0,
                                    border=0, border_radius=0,
                                    border_color=(255,0,0), label='Adult(s)',
                                    increase_decrease=True,
                                    min_max={'min':1,'max':10},
                                    content='1',
                                    content_position=Box.CENTERLEFT,label_size=(label_width,label_font),
                                    color=self.get_color(),
                                    button1_config={'color':self._header.get_color(),'content':'-','position':Box.CENTERLEFT,'size':{'width':50,'height':40}},
                                    button2_config={'color':self._header.get_color(),'content':'+','position':Box.CENTERRIGHT,'size':{'width':50,'height':40}})

        self.children_field = Field(parent=self.main_content,
                                    x=0,y=self.adults_field.y+self.adults_field.height,
                                    width=self.main_content.width,
                                    height=height,
                                    position=None,
                                    margin=0, padding=0,
                                    border=0, border_radius=0,
                                    border_color=(255,0,0), label='Children (5-15)',
                                    increase_decrease=True,
                                    min_max={'min':0,'max':6},
                                    content='0',
                                    content_position=Box.CENTERLEFT,label_size=(label_width,label_font),
                                    color=self.get_color(),
                                    button1_config={'color':self._header.get_color(),'content':'-','position':Box.CENTERLEFT,'size':{'width':50,'height':40}},
                                    button2_config={'color':self._header.get_color(),'content':'+','position':Box.CENTERRIGHT,'size':{'width':50,'height':40}})

        self.total_field = Field(parent=self.main_content,
                                    x=0,y=self.children_field.y+self.children_field.height,
                                    width=self.main_content.width,
                                    height=height,
                                    position=None,
                                    margin=0, padding=0,
                                    border=0, border_radius=0,
                                    border_color=(255,0,0), label='Total',
                                    content=chosen_ticket['price'],
                                    content_position=Box.CENTERLEFT,label_size=(label_width,label_font),
                                    color=self.get_color())

        # Create button to for payment
        self.pay_button = Button(parent=self.main_content, 
                                    x=0, y=0, width=350, 
                                    height=70, padding=20, border=0,
                                    content=get_translated_text('pay'),
                                    content_position='center',
                                    color=self._header.get_color(),
                                    position=Box.BOTTOMRIGHT)
        modified_ticket = {'departure_station':self.departure_field.input_box,
                            'destination':self.destination_field.input_box,
                            'date_of_travel':self.date_field.input_box,
                            'route':self.route_field.input_box,
                            'price':self.total_field.input_box,
                            'railcard':self.railcard_field.input_box,
                            'ticket_type':self.tickettype_field.input_box,
                            'adult(s)':self.adults_field.input_box,
                            'children (5-15)':self.children_field.input_box}
        self.pay_button.clicked(post, Event(pygame.MOUSEBUTTONUP,state='pay',ticket=modified_ticket))


    def __str__(self):
        return Background.__str__(self)+json.dumps(self.chosen_ticket)

    def resize(self, screen):
        Background.resize(self, screen)
        content = str(int(self.chosen_ticket['price'])*int(self.adults_field.input_box.content)+int(self.children_field.input_box.content)*int(0.7*int(self.chosen_ticket['price'])))
        content = list(content)
        if len(content) > 3:
            content.insert(-3,',')
        content_str = ''
        for i in content:
            content_str += i
        self.total_field.input_box.content = content_str

    def paint(self, screen):
        Background.paint(self, screen)
        if self.departure_field:
            self.departure_field.update(self.event,screen)
        if self.destination_field:
            self.destination_field.update(self.event,screen)
        if self.date_field:
            self.date_field.update(self.event,screen)
        if self.route_field:
            self.route_field.update(self.event,screen)
        if self.tickettype_field:
            self.tickettype_field.update(self.event,screen)
        if self.railcard_field:
            self.railcard_field.update(self.event,screen)
        if self.adults_field:
            self.adults_field.update(self.event,screen)
        if self.children_field:
            self.children_field.update(self.event,screen)
        if self.total_field:
            self.total_field.update(self.event,screen)
        if self.pay_button:
            self.pay_button.update(self.event, screen)

class CalendarBackground(Background):
    def __init__(self, surface):
        Background.__init__(self, 'calendar', surface=surface)
    
    def paint(self, screen):
        Background.paint(self, screen)

class RechargeBackground(Background):
    def __init__(self, surface):
        Background.__init__(self, 'smartcard', surface=surface)
        self.recharge_box = Box(parent=self.main_content,
                                x=0, y=0,
                                width=self.main_content.width,
                                height=self.main_content.height-self.title.height, 
                                padding=10,
                                margin=0,
                                border=0,
                                border_radius=0,
                                border_color=(255,0,0), 
                                content=get_filename('recharge.jpg'),
                                content_color=(0,0,0),
                                content_position=Box.TOPLEFT,
                                content_size=(900,600),
                                color=self.get_color(),
                                position=Box.BOTTOMLEFT,
                                interactable=False)
        self.recharge_text = Box(parent=self.recharge_box,
                                x=0, y=0,
                                width=self.main_content.width,
                                height=self.title.height, 
                                padding=10,
                                margin=0,
                                border=0,
                                border_radius=0,
                                border_color=(255,0,0), 
                                content=get_translated_text('recharge'),
                                content_color=(0,0,0),
                                content_position=Box.TOPRIGHT,
                                content_size=(),
                                color=self.get_color(),
                                position=Box.BOTTOMRIGHT,
                                interactable=False)
        self.recharge_arrow = Box(parent=self.recharge_box,
                                x=0, y=self.recharge_box.get_content_rect().height,
                                width=self.recharge_text.width,
                                height=self.recharge_box.height-self.recharge_box.get_content_rect().height-self.recharge_text.height, 
                                padding=10,
                                margin=0,
                                border=0,
                                border_radius=0,
                                border_color=(255,0,255), 
                                content=get_filename('right_arrow.png'),
                                content_color=(0,0,0),
                                content_position=Box.CENTER,
                                content_size=(),
                                color=self.get_color(),
                                position=None,
                                interactable=False)
    
    def paint(self, screen):
        Background.paint(self, screen)
        if self.recharge_box:
            self.recharge_box.draw(screen)
        if self.recharge_arrow:
            self.recharge_arrow.draw(screen)
        if self.recharge_text:
            self.recharge_text.draw(screen)

class TranslateBackground(Background):
    def __init__(self, surface):
        Background.__init__(self, 'translate', surface=surface)
        self.translations_box = Box(parent=self.main_content,
                        x=0, y=0, width=540,
                        height=400, padding=0,
                        margin=0, border=0,
                        border_radius=0,
                        border_color=(255,255,0), 
                        content=None,
                        content_color=(0,0,0),
                        content_position='center',
                        color=self.get_color(),
                        position=Box.CENTER,
                        interactable=False)
        self.english_button = Button(parent=self.translations_box, 
                        x=0, y=0, width=180, 
                        height=120, padding=2,
                        border=0,
                        content=get_filename('en_flag.png'),
                        content_position='center',
                        color=self.get_color(),
                        position=Box.TOPLEFT)
        self.english_button.clicked(post, Event(pygame.MOUSEBUTTONUP,state='translate',lang='en', desc='English'))
        self.english_text = Box(parent=self.translations_box,
                        x=0, y=0, width=180,
                        height=120, padding=20,
                        margin=0, border=0,
                        border_radius=0,
                        border_color=(255,255,0),
                        content='English',
                        content_color=(0,0,0),
                        content_position='center',
                        color=self.get_color(),
                        position=Box.TOPCENTER,
                        interactable=False)
        self.french_button = Button(parent=self.translations_box, 
                        x=0, y=0, width=180, 
                        height=120, padding=2,
                        border=0,
                        content=get_filename('fr_flag.png'),
                        content_position='center',
                        color=self.get_color(),
                        position=Box.CENTERLEFT)
        self.french_button.clicked(post, Event(pygame.MOUSEBUTTONUP,state='translate',lang='fr', desc='French'))
        self.french_text = Box(parent=self.translations_box,
                        x=0, y=0, width=180,
                        height=120, padding=20,
                        margin=0, border=0,
                        border_radius=0,
                        border_color=(255,255,0),
                        content='French',
                        content_color=(0,0,0),
                        content_position='center',
                        color=self.get_color(),
                        position=Box.CENTER,
                        interactable=False)
        self.pidgin_button = Button(parent=self.translations_box, 
                        x=0, y=0, width=180, 
                        height=120, padding=2,
                        border=0,
                        content=get_filename('pn_flag.png'),
                        content_position='center',
                        color=self.get_color(),
                        position=Box.BOTTOMLEFT)
        self.pidgin_button.clicked(post, Event(pygame.MOUSEBUTTONUP,state='translate',lang='pn', desc='Pidgin'))
        self.pidgin_text = Box(parent=self.translations_box,
                        x=0, y=0, width=180,
                        height=120, padding=20,
                        margin=0, border=0,
                        border_radius=0,
                        border_color=(255,255,0),
                        content='Pidgin',
                        content_color=(0,0,0),
                        content_position='center',
                        color=self.get_color(),
                        position=Box.BOTTOMCENTER,
                        interactable=False)

    def paint(self, screen):
        Background.paint(self, screen)
        if self.translations_box:
            self.translations_box.draw(screen)
        if self.english_button:
            self.english_button.update(self.event, screen)
        if self.english_text:
            self.english_text.draw(screen)
        if self.french_button:
            self.french_button.update(self.event, screen)
        if self.french_text:
            self.french_text.draw(screen)
        if self.pidgin_button:
            self.pidgin_button.update(self.event, screen)
        if self.pidgin_text:
            self.pidgin_text.draw(screen)

class PayBackground(Background):
    def __init__(self, modified_ticket, surface):
        Background.__init__(self, 'card_payment', surface=surface)
        self.modified_ticket = modified_ticket
        self.pay_box = Box(parent=self.main_content,
                                x=0, y=0,
                                width=self.main_content.width,
                                height=self.main_content.height-self.title.height, 
                                padding=10,
                                margin=0,
                                border=0,
                                border_radius=0,
                                border_color=(255,0,0), 
                                content=None,
                                content_color=(0,0,0),
                                content_position=Box.CENTER,
                                content_size=(500,400),
                                color=self.get_color(),
                                position=Box.BOTTOMCENTER,
                                interactable=False)
        self.nfc_box = Box(parent=self.pay_box,
                                x=0, y=0,
                                width=300,
                                height=240, 
                                padding=10,
                                margin=0,
                                border=0,
                                border_radius=0,
                                border_color=(255,0,0), 
                                content=get_filename('nfc.png'),
                                content_color=(0,0,0),
                                content_position=Box.TOPCENTER,
                                content_size=(300,240),
                                color=self.get_color(),
                                position=Box.TOPCENTER,
                                interactable=False)
        self.price_box = Box(parent=self.pay_box,
                                x=0, y=0,
                                width=300,
                                height=240, 
                                padding=10,
                                margin=0,
                                border=0,
                                border_radius=0,
                                border_color=(255,0,0), 
                                content=modified_ticket['price'].content,
                                content_color=(0,0,0),
                                content_position=Box.CENTER,
                                content_size=(500,400),
                                color=self.get_color(),
                                position=Box.CENTER,
                                interactable=False)
        self.pay_button = Button(parent=self.pay_box,
                                x=0, y=0,
                                width=200,
                                height=100, 
                                padding=10,
                                margin=0,
                                border=0,
                                border_radius=10,
                                border_color=(255,0,0), 
                                content='Pay',
                                content_color=(0,0,0),
                                content_position=Box.CENTER,
                                content_size=(),
                                color=self._header.get_color(),
                                position=Box.BOTTOMCENTER)
    
        self.back_button.clicked(post, Event(pygame.MOUSEBUTTONUP, state='chosen'))
        
    def paint(self, screen):
        Background.paint(self, screen)
        if self.pay_box:
            self.pay_box.draw(screen)
        if self.nfc_box:
            self.nfc_box.draw(screen)
        if self.price_box:
            self.price_box.draw(screen)
        if self.pay_button:
            self.pay_button.update(self.event, screen)