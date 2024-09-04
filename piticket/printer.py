try:
    import cups 
    from cups_notify import Subscriber, event 
except ImportError:
    cups = None 

import tempfile 
import subprocess
import os.path as osp 

import pygame 
from PIL import Image 
from piticket.utils import LOGGER

PRINTER_TASKS_UPDATED = pygame.USEREVENT + 1

class Printer:
    def __init__(self, name='default', max_pages=-1, options=None, counters=None):
        self._conn = cups.Connection() if cups else None 
        self._notifier = Subscriber(self._conn) if cups else None 
        self.name = None 
        self.max_pages = max_pages 
        self.options = options 
        self.count = counters 
        if not cups:
            LOGGER.warning('No printer found (pycups or pycups-notify not installed)')
            return # CUPS is not installed
        
        if not name or name.lower() == 'default':
            self.name = self._conn.getDefault()
            if not self.name and self._conn.getPrinters():
                self.name = list(self._conn.getPrinters().keys())[0]
        elif name in self._conn.getPrinters():
            self.name = name 

        if not self.name:
            if name.lower() == 'default':
                LOGGER.warning("No printer configured in CUPS (see http://localhost:631)")
            else:
                LOGGER.warning("No printer named '%s' in CUPS ")
        else:
            LOGGER.info("Connected to printer '%s'", self.name)
        
        if self.options and not isinstance(self.options, dict):
            LOGGER.warning("Invalid printer '%s', dict is expected", self.options)
            self.options = {}
        elif not self.options:
            self.options = {}

    def _on_event(self, evt):
        """Call for each new printer event.
        """
        LOGGER.info(evt.title)
        pygame.event.post(pygame.event.Event(PRINTER_TASKS_UPDATED, evt=evt))

    def is_installed(self):
        """Return True if the CUPS server is available for printing 
            and there is an available printer
        """
        return cups is not None and self.name is not None 

    def is_ready(self):
        """Return False if paper/ink counter is reached or printing is disabled
        """
        if not self.is_installed():
            return False 
        if self.max_pages < 0 or self.count is None:
            return True 
        return self.count.printed < self.max_pages 

    def is_connected(self):
        """Check if printer is connected through the usb port
        """
        p = subprocess.run(['lsusb'],capture_output=True)
        output = p.stdout.decode('utf-8').split('\n')
        for dev in output:
            dev = dev.lower()
            if 'jet' in dev or 'printer' in dev:
                return True
        return False
    
    def print_file(self, filename, copies=1):
        """Send a file to the CUPS server to the default printer.
        """
        if not self.name:
            raise EnvironmentError("No printer found (check config file or CUPS config)")
        if not osp.isfile(filename):
            raise IOError("No such file or directory: {}".format(filename))
        if self._notifier and not self._notifier.is_subscribed(self._on_event):
            self._notifier.subscribe(self._on_event, [event.CUPS_EVT_JOB_COMPLETED,
                                                    event.CUPS_EVT_JOB_CREATED,
                                                    event.CUPS_EVT_JOB_STOPPED,
                                                    event.CUPS_EVT_PRINTER_STATE_CHANGED,
                                                    event.CUPS_EVT_PRINTER_STOPPED])
        if copies > 1:
            pass
        else:
            self._conn.printFile(self.name, filename, osp.basename(filename), self.options)

    def cancel_all_tasks(self):
        """Cancel all tasks in the queue.
        """
        if not self.name:
            raise EnvironmentError("No printer found (check config file or CUPS config)")
        self._conn.cancelAllJobs(self.name)

    def get_all_tasks(self):
        """Return a dict (indexed by job ID) of dicts representing all tasks
        in the queue.
        """
        if not self.name:
            return {} # No printer found
        return self._conn.getJobs(my_jobs=True, requested_attributes=["job-id", "job-name", "job-uri", "job-state"])
    
    def quit(self):
        """Do cleanup actions.
        """
        if self._notifier:
            self._notifier.unsubscribe_all()
        