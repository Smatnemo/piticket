
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
    def state_wait_enter(self,cfg,app,win):
        win.drop_cache()

    @hookimpl 
    def state_wait_do(self,cfg,app,win):
        win.show_intro()

    @hookimpl 
    def state_wait_validate(self,cfg,app,win,events):
        change_event = app.find_event(events)
        if change_event:
            return 'choose'
        
    @hookimpl
    def state_choose_enter(self,cfg,app,win):
        """"""
        self.screen_lock_timer.start()

    @hookimpl 
    def state_choose_do(self,cfg,app,win,events):
        """"""
        event = app.find_button_event(events)
        win.show_choice(event, tickets=app.ticket_choices)
        if event:
            # Reset timer if cursor is active
            self.screen_lock_timer.start()
        if int(self.screen_lock_timer.remaining())==self.timeout and not events:
            win.show_popup_box('choose',self.timeout,app)
        
    @hookimpl
    def state_choose_validate(self,cfg,app,win,events):
        # Find event for next state
        change_event = app.find_change_event(events)  
        if change_event:
            if change_event.state == 'chosen':
                app.chosen_ticket = change_event.choice
            # Return to either choose, wait, translate, or chosen
            return change_event.state
        if self.screen_lock_timer.is_timeout():
            return 'wait'
        
    @hookimpl 
    def state_choose_exit(self,cfg,app,win):
        """"""

    @hookimpl 
    def state_chosen_enter(self,cfg,app,win):
        """"""
        self.screen_lock_timer.start()

    @hookimpl 
    def state_chosen_do(self,cfg,app,win,events):
        """"""
        event = app.find_button_event(events)
        win.show_choice(event,tickets=app.ticket_choices,selected=app.chosen_ticket)
        if event:
            # Reset timer if cursor is active
            self.screen_lock_timer.start()
        if int(self.screen_lock_timer.remaining())==self.timeout and not events:
            win.show_popup_box('chosen',self.timeout,app)

    @hookimpl 
    def state_chosen_validate(self,cfg,app,win,events):
        change_event = app.find_change_event(events)
        if change_event:
            # Return the state wait, choose, chosen
            return change_event.state

        if self.screen_lock_timer.is_timeout():
            return 'wait'

    @hookimpl 
    def state_chosen_exit(self,cfg,app,win):
        """"""

    @hookimpl
    def state_translate_enter(self,cfg,app,win):
        """"""

    @hookimpl 
    def state_translate_do(self,cfg,app,win,events):
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
    def state_translate_exit(self,cfg,app,win):
        """"""
        win.drop_cache()

    @hookimpl
    def state_future_tickets_enter(self,cfg,app,win):
        """"""

    @hookimpl 
    def state_future_tickets_do(self,cfg,app,win,events):
        """"""
        event = app.find_button_event(events)
        win.show_calendar(event)

    @hookimpl
    def state_future_tickets_validate(self,cfg,app,win,events):
        """"""
        change_event = app.find_change_event(events)
        if change_event:
            return change_event.state

    @hookimpl
    def state_future_tickets_exit(self,cfg,app,win):
        """"""


    @hookimpl 
    def state_recharge_do(self,cfg,app,win,events):
        """"""
        event = app.find_button_event(events)
        win.show_recharge(event)

    @hookimpl
    def state_recharge_validate(self,cfg,app,win,events):
        """"""
        change_event = app.find_change_event(events)
        if change_event:
            return change_event.state

    @hookimpl
    def state_pay_enter(self,cfg,app,win):
        """"""

    @hookimpl 
    def state_pay_do(self,cfg,app,win,events):
        """"""
        win.show_pay()

    @hookimpl
    def state_pay_validate(self,cfg,app,win,events):
        event = app.find_change_event(events)
        if event:
            return 'chosen'

    @hookimpl 
    def state_pay_exit(self,cfg,app,win):
        """"""