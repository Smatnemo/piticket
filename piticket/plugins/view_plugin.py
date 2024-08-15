from piticket import project_name 
from piticket import hookimpl 

class ViewPlugin():
    name = f'{project_name}-core:view'
    def __init__(self,plugin_manager):
        self.pm = plugin_manager 

    @hookimpl
    def state_sleep_enter(self,app,win):
        pass

    @hookimpl 
    def state_sleep_do(self,app,win,events):
        win.show_video()
    
    @hookimpl 
    def state_sleep_validate(self,app,win,events):
        event = app.find_change_event(events)
        if event:
            return 'wait'
    
    @hookimpl 
    def state_sleep_exit(self,app,win):
        pass

    @hookimpl 
    def state_wait_enter(self,app,win):
        pass 

    @hookimpl 
    def state_wait_do(self,app,win,events):
        win.show_intro()

    @hookimpl 
    def state_wait_validate(self,app,win,events):
        event = app.find_change_event(events)
        if event:
            return ''

    @hookimpl 
    def state_wait_exit(self,app,win):
        pass 