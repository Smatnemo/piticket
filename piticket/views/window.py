import pygame 
import os

class PiWindow():
    """Change backgrounds """

    FULLSCREEN = 'fullscreen'

    def __init__(self, title,
                bg_color=(0,0,0),
                size=(800, 480)):

        self.bg_color = bg_color 
        self.__size = size 
    
        if 'SDL_VIDEO_WINDOW_POS' not in os.environ:
            os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()

        # Get info of the screen using pygame
        display_info = pygame.display.Info()
        self.display_size = (display_info.current_w, display_info.current_h)

        # initialize display
        pygame.display.set_caption(title)
        self.is_fullscreen = False
        pygame.display.set_mode(self.__size, pygame.RESIZABLE)

    
        
        