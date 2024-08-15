from pluggy import HookspecMarker
from piticket import project_name 

hookspec = HookspecMarker(project_name)

@hookspec 
def state_wait_enter(app,win):
    """"""

@hookspec 
def state_wait_do(app,win,events):
    """"""

@hookspec(firstresult=True)
def state_wait_validate(app,win,events):
    """"""

@hookspec 
def state_wait_exit(app,win):
    """"""

@hookspec 
def state_choose_enter(app,win):
    """"""

@hookspec 
def state_choose_do(app,win,events):
    """"""

@hookspec(firstresult=True) 
def state_choose_validate(app,win,events):
    """"""

@hookspec 
def state_choose_exit(app,win):
    """"""

# @hookspec 
# def state_chosen_enter(app,win):
#     """"""

# @hookspec 
# def state_chosen_do(app,win,events):
#     """"""

# @hookspec(firstresult=True) 
# def state_chosen_validate(app,win,events):
#     """"""

# @hookspec 
# def state_chosen_exit(app,win):
#     """"""

# @hookspec 
# def state_pay_enter(app,win):
#     """"""

# @hookspec 
# def state_pay_do(app,win,events):
#     """"""

# @hookspec(firstresult=True) 
# def state_pay_validate(app,win,events):
#     """"""

# @hookspec 
# def state_pay_exit(app,win):
#     """"""

# @hookspec 
# def state_collect_enter(app,win):
#     """"""

# @hookspec 
# def state_collect_do(app,win,events):
#     """"""

# @hookspec(firstresult=True) 
# def state_collect_validate(app,win,events):
#     """"""

# @hookspec 
# def state_collect_exit(app,win):
#     """"""

# @hookspec 
# def state_recharge_enter(app,win):
#     """"""

# @hookspec 
# def state_recharge_do(app,win,events):
#     """"""

# @hookspec(firstresult=True) 
# def state_recharge_validate(app,win,events):
#     """"""

# @hookspec 
# def state_recharge_exit(app,win):
#     """"""

# @hookspec 
# def state_print_enter(app,win):
#     """"""

# @hookspec 
# def state_print_do(app,win,events):
#     """"""

# @hookspec(firstresult=True) 
# def state_print_validate(app,win,events):
#     """"""

# @hookspec 
# def state_print_exit(app,win):
#     """"""

# @hookspec 
# def state_finish_enter(app,win):
#     """"""

# @hookspec 
# def state_finish_do(app,win,events):
#     """"""

# @hookspec(firstresult=True) 
# def state_finish_validate(app,win,events):
#     """"""

# @hookspec 
# def state_finish_exit(app,win):
#     """"""