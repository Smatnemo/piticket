import time 
from piticket.utils import BlockConsoleHandler, LOGGER 

class StatesMachine():
    def __init__(self, plugin_manager, configuration, app, window):
        self.states = set()
        self.active_state = None
        self.failsafe_state = None
        self.pm = plugin_manager
        # Variables shared between states
        self.win = window 
        self.app = app
        self.cfg = configuration

        self._start_time = time.time()

    def add_state(self, name):
        """Add a unique state to the internal set.
        """
        self.states.add(name)

    def remove_state(self, name):
        """Remove a state from the internal set.
        """
        self.states.discard(name)
        if name == self.failsafe_state:
            self.failsafe_state = None 

    def process(self, events):
        """Execute the substates of the current state
        """
        # Run only when there is an active state
        if not self.active_state:
            return 
        
        try:
            # Execute the actions of the active state
            hook = getattr(self.pm.hook, f'state_{self.active_state}_do')
            hook(cfg=self.cfg,app=self.app,win=self.win,events=events)
            # Check conditions to move to the next state
            hook = getattr(self.pm.hook, f'state_{self.active_state}_validate')
            new_state_name = hook(cfg=self.cfg,app=self.app,win=self.win,events=events)
        except Exception as ex:
            if self.failsafe_state and self.active_state != self.failsafe_state:
                LOGGER.error(str(ex))
                LOGGER.debug('Back to failsafe state due to error:', exc_info=True)
                new_state_name = self.failsafe_state
            else:
                raise
        
        if new_state_name is not None:
            self.set_state(new_state_name)

    def set_state(self, state_name):
        """Change state machine's active state
        """
        try:
            # Perform any exit actions or clean up operations
            if self.active_state is not None:
                hook = getattr(self.pm.hook, f'state_{self.active_state}_exit')
                hook(cfg=self.cfg,app=self.app,win=self.win)
                BlockConsoleHandler.dedent()
                LOGGER.debug("took %0.3f secons", time.time() - self._start_time)
        except Exception as ex:
            if self.failsafe_state and self.active_state != self.failsafe_state:
                LOGGER.error(str(ex))
                LOGGER.debug('Back to failsafe state due to error:', exc_info=True)
            else:
                raise 

        if state_name not in self.states:
            raise ValueError(f'"{state_name}" not in registered states')

        # Switch to the new state and perform its entry actions
        BlockConsoleHandler.indent()
        self._start_time = time.time()
        LOGGER.debug("Active state '%s", state_name)
        self.active_state = state_name 

        try:
            hook = getattr(self.pm.hook, f'state_{self.active_state}_enter')
            hook(cfg=self.cfg,app=self.app,win=self.win)
        except Exception as ex:
            if self.failsafe_state and self.active_state != self.failsafe_state:
                LOGGER.error(str(ex))
                LOGGER.debug('Back to failsafe state due to error:', exc_info=True)
                self.set_state(self.failsafe_state)
            else:
                raise