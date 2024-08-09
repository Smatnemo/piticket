import pygame 
import os

from piticket.views import background

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
        
    def _update_background(self, bkgd, events=[]):
        # This allows a background to be initialized once and saved in the dictionary, backgrounds
        self.current_background = self.backgrounds.setdefault(str(bkgd), bkgd)
        self.current_background.set_color(self.bg_color)
        self.current_background.set_text_color(self.text_color)
        self.current_background.handle_events(events)
        self.current_background.resize(self.surface)
        self.current_background.paint(self.surface)

    def show_video(self, events):
        """Show video as screen saver in sleep mode
        """
        video = '/home/pi/Videos/big_buck_bunny_1080p_stereo.avi'
        self._update_background(background.VideoBackground(video), events)

    def show_intro(self):
        self._update_background(background.IntroBackground())

    