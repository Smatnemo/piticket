import multiprocessing
import pygame
import sys

import os.path as osp

PACKAGE_DIR = osp.abspath(osp.dirname(osp.dirname(__file__)))
sys.path.insert(0, PACKAGE_DIR)

from utils import *
from views import PiWindow

class PiApplication():
    def __init__(self):
        self.win = PiWindow('Ticket App')
    
    def _initialize(self):
        pass 

    def find_quit_event(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return event 
        return 

    def find_change_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                return event 
        return 
        
    def main_loop(self):
        try:
            clk = pygame.time.Clock()
            fps = 40
            self._initialize()

            start = True

            # Change to True to show background
            show_background = False

            while start:
                # Get events list 
                events = pygame.event.get()

                if self.find_quit_event(events):
                    start = False
                        
                # change background
                if self.find_change_event(events):
                    show_background = True 
                if show_background:
                    self.win.show_intro()
                else:
                    self.win.show_video(events)

                pygame.display.update()
                clk.tick(fps) # Ensure the program will never run more than 40 frames per second
            
        except Exception as ex:
            LOGGER.error(str(ex))
            LOGGER.error(get_crash_message())
        finally:
            pygame.quit()


def main():
    """Application entry point.
    """
    if hasattr(multiprocessing, 'set_start_method'):
        # Avoid use 'fork': safely forking a multithreaded process is problematic
        multiprocessing.set_start_method('spawn')
    configure_logging(msgfmt='[ %(levelname)-8s] %(name)-18s: %(message)s', filename='/tmp/piticket/piticket.log')
    app = PiApplication()
    app.main_loop()

    
if __name__ == '__main__':
    main()