import multiprocessing
from utils import *

class PiApplication():
    def __init__(self, cfg, pm):
        self._pm = pm 
        self._cfg = cfg
    
    def _initialize(self):
        pass 
        
    def main_loop():
        pass 

def main():
    """Application entry point.
    """
    if hasattr(multiprocessing, 'set_start_method'):
        # Avoid use 'fork': safely forking a multithreaded process is problematic
        multiprocessing.set_start_method('spawn')
    print(multiprocessing)
    configure_logging(msgfmt='[ %(levelname)-8s] %(name)-18s: %(message)s', filename='piticket.log')
    LOGGER.debug('Please check')
    LOGGER.info('Starting piticket')
    LOGGER.error('Crashing message')
if __name__ == '__main__':
    main()