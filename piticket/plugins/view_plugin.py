
import pygame
from piticket import project_name 
from piticket import hookimpl 
from piticket.language import change_language
from piticket.utils import PoolingTimer

class ViewPlugin():
    name = f'{project_name}-core:view'
    def __init__(self,plugin_manager):
        self.pm = plugin_manager 
        self.screen_lock_timer = PoolingTimer(60)
        # Default time for pop up box
        self.timeout = 10

    @hookimpl 
    def state_wait_enter(self,app,win):
        win.drop_cache()

    @hookimpl 
    def state_wait_do(self,app,win):
        win.show_intro()

    @hookimpl 
    def state_wait_validate(self,app,win,events):
        change_event = app.find_event(events)
        if change_event:
            return 'choose'
        
    @hookimpl
    def state_choose_enter(self,app,win):
        """"""
        self.screen_lock_timer.start()

    @hookimpl 
    def state_choose_do(self,app,win,events):
        """"""
        event = app.find_button_event(events)
        win.show_choice(event, tickets=travels)
        if event:
            # Reset timer if cursor is active
            self.screen_lock_timer.start()
        if int(self.screen_lock_timer.remaining())==self.timeout and not events:
            win.show_popup_box('choose',self.timeout,app)
        
    @hookimpl
    def state_choose_validate(self,app,win,events):
        # Find event for next state
        change_event = app.find_change_event(events)  
        if change_event:
            # Return to either choose, wait, translate, or chosen
            return change_event.state
        if self.screen_lock_timer.is_timeout():
            return 'wait'
        
    @hookimpl 
    def state_choose_exit(self,app,win):
        """"""
        # Clear event list before next cycle

    @hookimpl 
    def state_chosen_enter(self,app,win):
        """"""
        self.screen_lock_timer.start()

    @hookimpl 
    def state_chosen_do(self,app,win,events):
        """"""
        event = app.find_button_event(events)
        win.show_choice(event,tickets=travels,selected=('Nasarawa','₦10,000','Standard off-peak day return'))
        if event:
            # Reset timer if cursor is active
            self.screen_lock_timer.start()
        if int(self.screen_lock_timer.remaining())==self.timeout and not events:
            win.show_popup_box('chosen',self.timeout,app)

    @hookimpl 
    def state_chosen_validate(self,app,win,events):
        change_event = app.find_change_event(events)
        if change_event:
            # Return the state wait, choose, chosen
            return change_event.state

        if self.screen_lock_timer.is_timeout():
            return 'wait'

    @hookimpl 
    def state_chosen_exit(self,app,win):
        """"""

    @hookimpl
    def state_translate_enter(self,app,win):
        """"""

    @hookimpl 
    def state_translate_do(self,cfg, app,win,events):
        """"""
        event = app.find_button_event(events)
        win.show_translations(event)
    @hookimpl
    def state_translate_validate(self, cfg, app,win,events):
        """"""
        change_event = app.find_change_event(events)
        if change_event:
            if change_event.state=='translate':
                change_language(cfg, change_event.lang,  change_event.desc)
            return change_event.state

    @hookimpl 
    def state_translate_exit(self,app,win):
        """"""
        win.drop_cache()

    @hookimpl
    def state_pay_enter(self,app,win):
        """"""

    @hookimpl 
    def state_pay_do(self,app,win,events):
        """"""
        win.show_pay()

    @hookimpl
    def state_pay_validate(self,app,win,events):
        event = app.find_change_event(events)
        if event:
            return 'chosen'

    @hookimpl 
    def state_pay_exit(self,app,win):
        """"""
# The Symbol for Naira alt Code is 8358.
# Naira symbol not showing in render
# Dummy data for RowView
travels = {('Nasarawa','₦10,000','Standard off-peak day return'):{'departure_station':'Lagos','destination':'Abuja','date_of_travel':'09:18','route':'ANY PERMITTED','price':'10,000','ticket_type':'Standard off-peak day return','passengers':{'adult(s)':'1','children (5-15)':'1'}},
('Kaduna','₦20,000','Standard off-peak day return'):{'departure_station':'Lagos','destination':'Abuja','date_of_travel':'10:18','route':'ANY PERMITTED','price':'20,000','ticket_type':'Standard off-peak day return','passengers':{'adult(s)':'1','children (5-15)':'0'}},
('Niger','₦15,000','Standard off-peak day return'):{'departure_station':'Lagos','destination':'Abuja','date_of_travel':'12:18','route':'ANY PERMITTED','price':'15,000','ticket_type':'Standard off-peak day return','passengers':{'adult(s)':'2','children (5-15)':'2'}},
('Kogi','₦30,000','Standard off-peak day return'):{'departure_station':'Lagos','destination':'Abuja','date_of_travel':'13:50','route':'ANY PERMITTED','price':'30,000','ticket_type':'Standard off-peak day return','passengers':{'adult(s)':'3','children (5-15)':'0'}},
('Lagos','₦12,000','Standard off-peak day return'):{'departure_station':'Lagos','destination':'Abuja','date_of_travel':'15:60','route':'ANY PERMITTED','price':'12,000','ticket_type':'Standard off-peak day return','passengers':{'adult(s)':'2','children (5-15)':'3'}}}
# For choose state and quick display use destination, type, price