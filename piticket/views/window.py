import pygame 
import os

from pygame.event import post, Event
from piticket.views import background
from piticket.utils import LOGGER
from piticket.language import get_translated_text
from piticket.payment_terminal import PAYMENT_STATUS_EVENT
from piticket.views.box import PopUpBox, PopUpBoxProcessing

class PiWindow():
    """Change backgrounds """

    FULLSCREEN = 'fullscreen'

    def __init__(self, title,
                bg_color=(255,255,255),
                text_color=(0,0,0),
                size=(1280, 1000)):

        self.bg_color = bg_color 
        self.__size = size
        self.text_color = text_color  
    
        if 'SDL_VIDEO_WINDOW_POS' not in os.environ:
            os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()

        # Get info of the screen using pygame
        display_info = pygame.display.Info()
        self.display_size = (display_info.current_w, display_info.current_h)
        
        # initialize display
        pygame.display.set_caption(title)
        self.is_fullscreen = False
        self.surface = pygame.display.set_mode(self.__size, pygame.RESIZABLE)

        self.backgrounds = {}
        self.current_background = None

        self._popup_box = None
        self._popup_box_process = None 
        

    def _update_background(self, bkgd, event=None):
        # This allows a background to be initialized once and saved in the dictionary, backgrounds
        self.current_background = self.backgrounds.setdefault(str(bkgd), bkgd)
        self.current_background.set_color(self.bg_color)
        self.current_background.set_text_color(self.text_color)
        self.current_background.handle_events(event)
        self.current_background.resize(self.surface)
        self.current_background.paint(self.surface)

    def show_intro(self):
        """Show video as screen saver in sleep mode
        """
        video = '/home/pi/Videos/big_buck_bunny_1080p_stereo.avi'
        if os.path.isfile(video):
            self._update_background(background.VideoBackground(video, self.surface))
        else:
            self._update_background(background.IntroBackground(self.surface))

    
    def show_choice(self, events, tickets={}, selected=None):
        """Display all choices when nothing is selected
        :param event: filtered event for button actions
        :type event: pygame.event.Event
        :param tickets: ticket information from backoffice
        :type tickets: dict
        :param selected: tuple for hashing the dictionary for specific ticket used in Chosen Background
        :type selected: tuple
        """
        if not selected:
            self._update_background(background.ChooseBackground(tickets, self.surface), events)
        else:
            self._update_background(background.ChosenBackground(selected, self.surface), events)

    def show_calendar(self, event):
        """Display dates using a calendar.
        :param event: event for button effects
        :type event: pygame.event.Event
        """
        self._update_background(background.CalendarBackground(self.surface), event)

    def show_processing(self):
        """Display while building ticket
        """
        self._update_background(background.ProcessingBackground(self.surface))
        
    def show_translations(self, event):
        """Display a list of available translations. Choose a language
        :param event: event for button effects
        :type event: pygame.event.Event
        """
        self._update_background(background.TranslateBackground(self.surface), event)
    
    def show_recharge(self, event):
        """Display option for recharging smart card.
        :param event: event for button effects
        :type event: pygame.event.Event
        """
        self._update_background(background.RechargeBackground(self.surface), event)

    def show_pay(self, event, filename, modified_ticket):
        """Display instructions for payment
        :param filename: the temporary filename where the ticket is stored.
                    Read for display
        :type filename: str
        :param modified_ticket: details chosen by the user
        :type modified_ticket: dict
        """
        self._update_background(background.PayBackground(filename, modified_ticket, self.surface), event)

    def show_printing(self):
        """Display when printing ticket
        """
        self._update_background(background.PrintBackground(self.surface))

    def show_payment_status(self, successful=True):
        """Display the status of the payment.
        """
        if successful:
            self._update_background(background.PaymentSuccessfulBackground(self.surface))
        else:
            self._update_background(background.PaymentFailedBackground(self.surface))
        
    def show_popup_box(self, state_name, timeout, app):
        """Show a pop up box on any state.
        :param state_name: the name of the state calling the pop up box
        :type state_name: str
        :param timeout: the duration for which the pop up box will be shown on the screen
        :type timeout: int
        :param app: the main pi application 
        :type app: PiApplication
        """
        self._popup_box = PopUpBox(parent=self.surface, width=400, height=300,
                                    content_color=(127,127,127), color=self.bg_color, timeout=timeout)
        # End pop up box when Yes button is clicked and return to to same state
        self._popup_box.btn1.clicked(app.post_event, state_name)
        # End pop up box when No button is clicked and return to wait state
        self._popup_box.btn2.clicked(app.post_event, 'wait')
        # End pop up box after timeout duration
        self._popup_box.triggered(app.post_event, 'wait')

        while self._popup_box.started:
            events = pygame.event.get()
            self._popup_box.update(events, self.surface)
            pygame.display.update()

        self._popup_box = None
    
    def show_popup_processing_box(self, text):
        """Create a pop up box with a gif for progress
        :param text: the key for translated text to be used when showing progress
        :type text: str"""        
        self._popup_box = PopUpBoxProcessing(event=Event(PAYMENT_STATUS_EVENT,),
                                            post_event=True, 
                                            parent=self.surface,
                                            gif_image='Spinner_transparent',
                                            x=0, y=0,
                                            width=400, height=300,
                                            position='center',
                                            margin=20, padding=10,
                                            border=1, border_radius=3,
                                            border_color=(0,0,0),
                                            content=get_translated_text(text),
                                            content_color=self.text_color,
                                            content_position='top-center',
                                            content_size=(),
                                            color=self.bg_color,
                                            interactable=False)
        # self._popup_box.triggered(post, Event(pygame.MOUSEBUTTONUP, status='approved', state=state_name))
        while self._popup_box.started:
            events = pygame.event.get()
            self._popup_box.update(events, self.surface)
            pygame.display.update()
        self._popup_box = None

    def show_finish(self):
        self._update_background(background.FinishedBackground(self.surface))

    def drop_cache(self):
        """Drop all cached background and foreground to force refreshing the view.
        """
        self.current_background = None 
        self.backgrounds = {}
