import multiprocessing
import pygame
from utils import *
from views import PiWindow

class PiApplication():
    def __init__(self):
        self.win = PiWindow('Ticket App')
    
    def _initialize(self):
        pass 
        
    def main_loop(self):
        clk = pygame.time.Clock()
        fps = 40
        start = True

        while start:
            events = pygame.event.get()
            # if pygame.event.QUIT()
            for event in events:
                if event.type == pygame.QUIT:
                    start = False
            pygame.display.update()
            clk.tick(fps) # Ensure the program will never run more than 40 frames per second
        LOGGER.debug('Please check')
        LOGGER.info('Starting piticket')
        LOGGER.error('Crashing message')

def main():
    """Application entry point.
    """
    if hasattr(multiprocessing, 'set_start_method'):
        # Avoid use 'fork': safely forking a multithreaded process is problematic
        multiprocessing.set_start_method('spawn')
    configure_logging(msgfmt='[ %(levelname)-8s] %(name)-18s: %(message)s', filename='piticket.log')
    app = PiApplication()
    app.main_loop()

    
if __name__ == '__main__':
    main()