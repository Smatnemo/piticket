from piticket import project_name 
from piticket import hookimpl 
from piticket.utils import PoolingTimer

class ViewPlugin():
    name = f'{project_name}-core:view'
    def __init__(self,plugin_manager):
        self.pm = plugin_manager 
        self.screen_lock_timer = PoolingTimer(30)
        # Default time for pop up box
        self.timeout = 10

    @hookimpl 
    def state_wait_enter(self,app,win):
        pass 

    @hookimpl 
    def state_wait_do(self,app,win,events):
        win.show_intro()

    @hookimpl 
    def state_wait_validate(self,app,win,events):
        event = app.find_event(events)
        if event:
            return 'choose'

    @hookimpl 
    def state_wait_exit(self,app,win):
        pass 

    @hookimpl
    def state_choose_enter(self,app,win):
        """"""
        self.screen_lock_timer.start()

    @hookimpl 
    def state_choose_do(self,app,win,events):
        """"""
        win.show_choice()
        if int(self.screen_lock_timer.remaining())==self.timeout:
            win.show_popup_box('choose',self.timeout,app)

    @hookimpl
    def state_choose_validate(self,app,win,events):
        # Find event for next state
        change_event = app.find_change_event(events)  
        if change_event:
            if change_event.state=='chosen':
                return 'chosen'
            if change_event.state=='choose':
                return 'choose'
        if self.screen_lock_timer.is_timeout():
            return 'wait'
        
    @hookimpl 
    def state_choose_exit(self,app,win):
        """"""

    @hookimpl 
    def state_chosen_enter(self,app,win):
        """"""

    @hookimpl 
    def state_chosen_do(self,app,win,events):
        """"""
        win.show_choice()

    @hookimpl 
    def state_chosen_validate(self,app,win,events):
        event = app.find_change_event(events)
        if event:
            return 'pay'

    @hookimpl 
    def state_chosen_exit(self,app,win):
        """"""

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