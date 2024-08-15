from piticket import project_name 
from piticket import hookimpl 

class ViewPlugin():
    name = f'{project_name}-core:view'
    def __init__(self,plugin_manager):
        self.pm = plugin_manager 

    @hookimpl 
    def state_wait_enter(self,app,win):
        pass 

    @hookimpl 
    def state_wait_do(self,app,win,events):
        win.show_video()

    @hookimpl 
    def state_wait_validate(self,app,win,events):
        event = app.find_change_event(events)
        if event:
            return 'choose'

    @hookimpl 
    def state_wait_exit(self,app,win):
        pass 

    @hookimpl
    def state_choose_enter(self,app,win):
        """"""

    @hookimpl 
    def state_choose_do(self,app,win,events):
        """"""
        win.show_intro()

    @hookimpl
    def state_choose_validate(self,app,win,events):
        chosen_event = app.find_change_event(events)
        # recharge_event = app.find_change_event(events)
        if chosen_event:
            return 'chosen'
        # if recharge_event:
        #     return 'recharge'
        
    @hookimpl 
    def state_choose_exit(self,app,win):
        """"""

    # @hookspec 
    # def state_chosen_enter(self,app,win):
    #     """"""

    # @hookspec 
    # def state_chosen_do(self,app,win,events):
    #     """"""

    # @hookspec(firstresult=True) 
    # def state_chosen_validate(self,app,win,events):
    #     event = app.find_change_event(events)
    #     if event:
    #         return 'pay'

    # @hookspec 
    # def state_chosen_exit(self,app,win):
    #     """"""

    # @hookspec 
    # def state_pay_enter(self,app,win):
    #     """"""

    # @hookspec 
    # def state_pay_do(self,app,win,events):
    #     """"""

    # @hookspec(firstresult=True) 
    # def state_pay_validate(self,app,win,events):
    #     event = app.find_change_event(events)
    #     if event:
    #         return 'chosen'

    # @hookspec 
    # def state_pay_exit(self,app,win):
    #     """""