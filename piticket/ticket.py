import multiprocessing
import pygame
import sys
import tempfile
import logging

import os.path as osp

PROJECT_DIR = osp.abspath(osp.dirname(__file__))
PACKAGE_DIR, project_name = osp.split(PROJECT_DIR)
sys.path.insert(0, PACKAGE_DIR)

from piticket import language
from piticket.utils import *
from piticket.views import PiWindow
from piticket.states import StatesMachine
from piticket.config import PiConfigParser
from piticket.plugins import create_plugin_manager

# The Symbol for Naira alt Code is 8358.
# Naira symbol not showing in render
# Dummy data for RowView
travels = {('Nasarawa','10000','Standard off-peak day return'):{'departure_station':'Lagos','destination':'Nasarawa','date_of_travel':'09:18','route':'ANY PERMITTED','price':'10000','railcard':'25-30','ticket_type':'Standard off-peak day return','passengers':{'adult(s)':'1','children (5-15)':'1'}},
('Kaduna','20000','Standard off-peak day return'):{'departure_station':'Lagos','destination':'Kaduna','date_of_travel':'10:18','route':'ANY PERMITTED','price':'20000','railcard':'25-30','ticket_type':'Standard off-peak day return','passengers':{'adult(s)':'1','children (5-15)':'0'}},
('Niger','15000','Standard off-peak day return'):{'departure_station':'Lagos','destination':'Niger','date_of_travel':'12:18','route':'ANY PERMITTED','price':'15000','railcard':'25-30','ticket_type':'Standard off-peak day return','passengers':{'adult(s)':'2','children (5-15)':'2'}},
('Kogi','30000','Standard off-peak day return'):{'departure_station':'Lagos','destination':'Kogi','date_of_travel':'13:50','route':'ANY PERMITTED','price':'30000','railcard':'25-30','ticket_type':'Standard off-peak day return','passengers':{'adult(s)':'3','children (5-15)':'0'}},
('Ibadan','12000','Standard off-peak day return'):{'departure_station':'Lagos','destination':'Ibadan','date_of_travel':'15:60','route':'ANY PERMITTED','price':'12000','railcard':'25-30','ticket_type':'Standard off-peak day return','passengers':{'adult(s)':'2','children (5-15)':'3'}}}
# For choose state and quick display use destination, type, price

class PiApplication():
    def __init__(self, plugin_manager,config):
        self.win = PiWindow('Piticket')
        self._pm = plugin_manager

        self.chosen_ticket = None
        self.ticket_choices = travels

        self.active_state = None 
        self.previous_state = None

        self.payment_status = None
        
        self.states_machine = StatesMachine(self._pm,config,self,self.win)
        self.states_machine.add_state('wait')
        self.states_machine.add_state('choose')
        
        self.states_machine.add_state('chosen')
        self.states_machine.add_state('collect')
        self.states_machine.add_state('recharge')
        self.states_machine.add_state('translate')
        self.states_machine.add_state('future_tickets')

        self.states_machine.add_state('pay')
        self.states_machine.add_state('process')
        self.states_machine.add_state('print')
        self.states_machine.add_state('finish')

    def _initialize(self):
        pass 
    
    def post_event(self, state_name):
        """Place an event in the event list.
        """
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP,state=state_name))


    def find_quit_event(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return event 
        return 

    def find_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                return event 
        return 
    
    def find_change_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and hasattr(event, 'state'):
                return event
        return 

    def find_button_event(self, events):
        """Filter event for button effects and trigger
        """
        for event in events:
            if (event.type == pygame.MOUSEBUTTONDOWN\
                    or event.type == pygame.MOUSEBUTTONUP\
                    or event.type == pygame.MOUSEMOTION) and not hasattr(event,'state'):
                return event 
        return
        
    def main_loop(self):
        try:
            clk = pygame.time.Clock()
            fps = 40
            self._initialize()
            self.states_machine.set_state('wait')
            self.active_state = 'wait'

            start = True

            while start:
                # Get events list 
                events = pygame.event.get()

                if self.find_quit_event(events):
                    start = False
                        
                # Move between states
                self.states_machine.process(events)

                pygame.display.update()
                clk.tick(fps) # Ensure the program will never run more than 40 frames per second
            
        except Exception as ex:
            LOGGER.error(str(ex), exc_info=True)
            LOGGER.error(get_crash_message())
        finally:
            pygame.quit()


def main():
    """Application entry point.
    """
    if hasattr(multiprocessing, 'set_start_method'):
        # Avoid use 'fork': safely forking a multithreaded process is problematic
        multiprocessing.set_start_method('spawn')

    filename = osp.join(tempfile.gettempdir(),'piticket.log')
    configure_logging(logging.INFO, msgfmt='[ %(levelname)-8s] %(name)-18s: %(message)s', filename=filename)

    pm = create_plugin_manager(project_name)
    pm.load_all_plugins(paths=[],disabled=[])
    # Create config
    config = PiConfigParser('/home/pi/.config/piticket/piticket.cfg', pm, True)
    if not osp.isfile(config.filename):
        config.save(default=True)
    # initialize translations system
    language.change_language(config, config.get('GENERAL','language'))
    language.init('~/.config/piticket/translations.cfg', True)

    app = PiApplication(pm, config)
    app.main_loop()

    
if __name__ == '__main__':
    main()