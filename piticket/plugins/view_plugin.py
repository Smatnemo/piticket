
import time
import pygame
import os.path as osp
from piticket import project_name 
from piticket import hookimpl 
from piticket.language import change_language
from piticket.utils import PoolingTimer, LOGGER

class ViewPlugin():
    name = f'{project_name}-core:view'
    def __init__(self,plugin_manager):
        self.pm = plugin_manager 
        self.screen_lock_timer = PoolingTimer(60)
        self.finish_view_timer = PoolingTimer(5)
        self.print_view_timer = PoolingTimer(10)
        self.process_view_timer = PoolingTimer(5)
        # Default time for pop up box
        self.timeout = 10
        # self.modified_ticket=None

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
        win.show_choice(events, tickets=app.ticket_choices)
        if events:
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
        win.show_choice(events,selected=app.chosen_ticket)
        if events:
            # Reset timer if cursor is active
            self.screen_lock_timer.start()
        if int(self.screen_lock_timer.remaining())==self.timeout and not events:
            win.show_popup_box('chosen',self.timeout,app)

    @hookimpl 
    def state_chosen_validate(self,cfg,app,win,events):
        change_event = app.find_change_event(events)
        if change_event:
            if change_event.state=='process':
                app.modified_ticket=change_event.ticket
            # Return the state wait, choose, chosen, process
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
        win.show_translations(events)

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
        win.show_calendar(events)

    @hookimpl
    def state_future_tickets_validate(self,cfg,app,win,events):
        """"""
        change_event = app.find_change_event(events)
        if change_event:
            return change_event.state

    @hookimpl 
    def state_recharge_do(self,cfg,app,win,events):
        """"""
        win.show_recharge(events)

    @hookimpl
    def state_recharge_validate(self,cfg,app,win,events):
        """"""
        change_event = app.find_change_event(events)
        if change_event:
            return change_event.state

    @hookimpl
    def state_process_enter(self,cfg,app,win):
        """"""
        self.process_view_timer.start()
        win.show_processing()

    @hookimpl
    def state_process_validate(self,cfg,app,win,events):
        if app.ticket_file and osp.isfile(app.ticket_file.name):
            return 'pay'
            
    @hookimpl 
    def state_pay_enter(self,app):
        self.screen_lock_timer.start()

    @hookimpl 
    def state_pay_do(self,cfg,app,win,events):
        """"""
        win.show_pay(events, app.ticket_file.name, app.modified_ticket)
        event = app.process_payment(events)
        if event and event.status=='processing':
            win.show_popup_processing_box('process')

        if int(self.screen_lock_timer.remaining())==self.timeout and not events:
            win.show_popup_box('pay',self.timeout,app)

    @hookimpl
    def state_pay_validate(self,cfg,app,win,events):
        # Process back button and cancel buttons here
        change_event = app.find_change_event(events)
        if change_event:
            return change_event.state
        # Process payment event here
        payment_event = app.process_payment(events)
        if payment_event and payment_event.status != 'processing':
            if payment_event.status == 'approved':
                app.payment_status = True
            if payment_event.status == 'failed':
                app.payment_status = False
            return 'payment_process'
        
        if self.screen_lock_timer.is_timeout():
            return 'wait'
            

    @hookimpl
    def state_payment_process_enter(self,cfg,app,win):
        """"""
        self.process_view_timer.start()
        win.show_payment_status(successful=app.payment_status)

    @hookimpl
    def state_payment_process_do(self,cfg,app,win):
        """"""
        # Called here to keep updating time
        win.show_payment_status(successful=app.payment_status)

    @hookimpl
    def state_payment_process_validate(self,cfg,app,win,events):
        if self.process_view_timer.is_timeout():
            if app.payment_status:
                return 'print'
            else:
                return 'pay'

    @hookimpl
    def state_print_enter(self,cfg,app,win):
        """"""
        self.print_view_timer.start()
        win.show_printing()

    @hookimpl 
    def state_print_do(self,win):
        """"""
        win.show_printing()

    @hookimpl
    def state_print_validate(self,cfg,app,win,events):
        if self.print_view_timer.is_timeout():
            return 'finish'

    @hookimpl 
    def state_print_exit(self,cfg,app,win):
        """"""

    @hookimpl
    def state_finish_enter(self,cfg,app,win):
        """"""
        self.finish_view_timer.start()
        win.show_finish()

    @hookimpl
    def state_finish_validate(self,cfg,app,win,events):
        if self.finish_view_timer.is_timeout():
            return 'wait'