from pluggy import HookspecMarker
from piticket import project_name 

hookspec = HookspecMarker(project_name)

@hookspec 
def state_sleep_enter(app,win):
    """"""

@hookspec 
def state_sleep_do(app,win,events):
    """"""

@hookspec(firstresult=True)
def state_sleep_validate(app,win,events):
    """"""

@hookspec 
def state_sleep_exit(app,win):
    """"""

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