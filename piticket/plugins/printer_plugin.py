
import time 
import tempfile
import os.path as osp
from datetime import datetime
from piticket import hookimpl
from piticket.pictures import get_filename
from piticket.pictures.factory import get_ticket_factory 
from piticket.utils import LOGGER

class PrinterPlugin:

    name = 'piticket-core:printer'

    def __init__(self, plugin_manager):
        self._pm = plugin_manager

    def print_ticket(self, app):
        LOGGER.info("Send final ticket to printer")
        if osp.isfile(app.ticket_file):
            app.printer.print_file(app.ticket_file, app.print_copies)
        app.count += 1

    def build_ticket(self, app):
        # Get current time and date
        d = datetime.fromtimestamp(time.time())
        time_stamp = f"{d.strftime('%d/%m/%y  %H:%M:%S')}"

        app.modified_ticket.setdefault('date_printed',time_stamp)
        default_factory = get_ticket_factory(get_filename(app.ticket_template), app.modified_ticket)
        
        factory = self._pm.hook.piticket_setup_ticket_factory(factory=default_factory)
        app.ticket_file = time_stamp[-8:]
        factory.save(app.ticket_file)
    
    @hookimpl(hookwrapper=True)
    def piticket_setup_ticket_factory(self, factory):
        outcome = yield # invoke all corresponding hookimpls here
        factory = outcome.get_result() or factory
        outcome.force_result(factory)

    @hookimpl 
    def state_process_enter(self, app):
        self.build_ticket(app)

    @hookimpl 
    def state_process_exit(self, app):
        """Cleanup ticket before proceeding to print
        """
        app.modified_ticket = {}

    @hookimpl
    def state_print_enter(self, app):
        self.print_ticket(app)

    @hookimpl 
    def state_print_exit(self, app):
        """Cleanup before exiting print state"""