import pygame 
import os

from piticket.views import background
from piticket.views.box import PopUpBox, PopUpBoxProcessing

class PiWindow():
    """Change backgrounds """

    FULLSCREEN = 'fullscreen'

    def __init__(self, title,
                bg_color=(255,0,0),
                text_color=(255,255,255),
                size=(800, 480)):

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
        self._popup_box_process = PopUpBoxProcessing(event=None, parent=self.surface,gif_image='Spinner_transparent')

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
            self._update_background(background.VideoBackground(video))
        else:
            self._update_background(background.IntroBackground(self.surface))

    def show_choice(self, selected=None):
        if not selected:
            self._update_background(background.ChooseBackground(self.surface))
        else:
            self._update_background(background.ChosenBackground(self.surface))

    def show_popup_box(self, state_name, timeout, app):
        """Show a pop up box on any state.
        :param state_name: the name of the state calling the pop up box
        :type state_name: str
        :param timeout: the duration for which the pop up box will be shown on the screen
        :type timeout: int
        :param app: the main pi application 
        :type app: PiApplication
        """
        self._popup_box = PopUpBox(parent=self.surface, timeout=timeout)
        # End pop up box when Yes button is clicked and return to to same state
        self._popup_box.btn1.clicked(self.post_event, state_name)
        # End pop up box when No button is clicked and return to wait state
        self._popup_box.btn2.clicked(print_func, 'Clicked No Button')
        # End pop up box after timeout duration
        self._popup_box.triggered(print_func, 'Triggered at the end of PopUp')

        while self._popup_box.started:
            events = pygame.event.get()
            event = app.find_button_event(events)
            self._popup_box.update(event, self.surface)
            pygame.display.update()

        self._popup_box = None

    def post_event(self, state_name):
        """Place an event in the event list.
        """
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP,state=state_name))

# To end pop up box, set _started = False 
# To change state, use pygame.MOUSEBUTTONUP with custom attribute of state name
def print_func(*arg):
    print(*arg)