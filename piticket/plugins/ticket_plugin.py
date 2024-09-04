from piticket import hookimpl

class TicketPlugin:
    def __init__(self, plugin_manager):
        self._pm = plugin_manager

    @hookimpl
    def state_process_do(self, app):
        if app.payment_status:
            pass