from pluggy import HookspecMarker
from piticket import project_name 

hookspec = HookspecMarker(project_name)

@hookspec(firstresult=True)
def piticket_setup_ticket_factory(factory):
    """Setup factory for building ticket
    """
    
@hookspec 
def state_wait_enter(cfg,app,win):
    """"""

@hookspec 
def state_wait_do(cfg,app,win,events):
    """"""

@hookspec(firstresult=True)
def state_wait_validate(cfg,app,win,events):
    """"""

@hookspec 
def state_wait_exit(cfg,app,win):
    """"""



@hookspec 
def state_choose_enter(cfg,app,win):
    """"""

@hookspec 
def state_choose_do(cfg,app,win,events):
    """"""

@hookspec(firstresult=True) 
def state_choose_validate(cfg,app,win,events):
    """"""

@hookspec 
def state_choose_exit(cfg,app,win):
    """"""



@hookspec 
def state_chosen_enter(cfg,app,win):
    """"""

@hookspec 
def state_chosen_do(cfg,app,win,events):
    """"""

@hookspec(firstresult=True) 
def state_chosen_validate(cfg,app,win,events):
    """"""

@hookspec 
def state_chosen_exit(cfg,app,win):
    """"""


@hookspec 
def state_translate_enter(cfg,app,win):
    """"""

@hookspec 
def state_translate_do(cfg,app,win,events):
    """"""

@hookspec(firstresult=True) 
def state_translate_validate(cfg,app,win,events):
    """"""

@hookspec 
def state_translate_exit(cfg,app,win):
    """"""


@hookspec 
def state_recharge_enter(cfg,app,win):
    """"""

@hookspec 
def state_recharge_do(cfg,app,win,events):
    """"""

@hookspec(firstresult=True) 
def state_recharge_validate(cfg,app,win,events):
    """"""

@hookspec 
def state_recharge_exit(cfg,app,win):
    """"""



@hookspec 
def state_future_tickets_enter(cfg,app,win):
    """"""

@hookspec 
def state_future_tickets_do(cfg,app,win,events):
    """"""

@hookspec(firstresult=True) 
def state_future_tickets_validate(cfg,app,win,events):
    """"""

@hookspec 
def state_future_tickets_exit(cfg,app,win):
    """"""


@hookspec 
def state_process_enter(cfg,app,win):
    """Display processing while building the ticket.
    """

@hookspec 
def state_process_do(cfg,app,win,events):
    """"""

@hookspec(firstresult=True) 
def state_process_validate(cfg,app,win,events):
    """"""

@hookspec 
def state_process_exit(cfg,app,win):
    """"""




@hookspec 
def state_pay_enter(cfg,app,win):
    """"""

@hookspec 
def state_pay_do(cfg,app,win,events):
    """"""

@hookspec(firstresult=True) 
def state_pay_validate(cfg,app,win,events):
    """"""

@hookspec 
def state_pay_exit(cfg,app,win):
    """"""



@hookspec 
def state_payment_process_enter(cfg,app,win):
    """Display payment status. Either successful or Failed. Return to pay state if 
        failed and go to print state if successful.
    """

@hookspec 
def state_payment_process_do(cfg,app,win,events):
    """"""

@hookspec(firstresult=True) 
def state_payment_process_validate(cfg,app,win,events):
    """"""

@hookspec 
def state_payment_process_exit(cfg,app,win):
    """"""



@hookspec 
def state_print_enter(cfg,app,win):
    """"""

@hookspec 
def state_print_do(cfg,app,win,events):
    """"""

@hookspec(firstresult=True) 
def state_print_validate(cfg,app,win,events):
    """"""

@hookspec 
def state_print_exit(cfg,app,win):
    """"""



@hookspec 
def state_finish_enter(cfg,app,win):
    """"""

@hookspec 
def state_finish_do(cfg,app,win,events):
    """"""

@hookspec(firstresult=True) 
def state_finish_validate(cfg,app,win,events):
    """"""

@hookspec 
def state_finish_exit(cfg,app,win):
    """"""