import os
import sys 
import time
import logging
import platform


import os.path as osp
from piticket.fonts import get_pygame_font
from piticket import project_name

LOGGER = logging.getLogger(project_name)

class PoolingTimer():
    """Time to be checked in a pooling loop to check if time has been exceeded
    """
    def __init__(self, timeout, start=True):
        self.timeout = timeout 
        self.time = None 
        self._paused_total = 0
        self._paused_time = None 
        if start:
            self.start()
    
    def __enter__(self):
        """Start timer if used as context manager."""
        self.start()
        return self 
    
    def __exit__(self, *args):
        """Stop timer if used as context manager"""
        self.time = None 

    def reset(self):
        """Restart timer to its initial state"""
        self.time = None 
        self._paused_total = 0
        self._paused_time = None 

    def start(self):
        """Start the timer"""
        if self.timeout < 0:
            raise ValueError("PoolingTimer cannot be started if timeout is less than 0")
        if self._paused_time:
            self._paused_total += time.time() - self._paused_time 
            self._paused_time = None 
        else:
            self._paused_total = 0 
            self.time = time.time()
    
    def freeze(self):
        """Pause the timer.
        """
        if not self._paused_time:
            self._paused_time = time.time()
        
    def remaining(self):
        """Return the remaining seconds
        """
        if self.time is None:
            remain = float(self.timeout)
        else:
            remain = self.timeout + self.paused() - (time.time() - self.time)
            if remain < 0.0:
                remain = 0.0 
        return remain 

    def paused(self):
        """Return the pause duration in seconds.
        """
        if self._paused_time:
            return self._paused_total + time.time() - self._paused_time 
        return self._paused_total

    def elapsed(self):
        """Return the elapsed
        """
        if self.time is None:
            return 0.0
        return time.time() - self.time - self.paused()

    def is_timeout(self):
        """Return True if the timer is in timeout.
        """
        elapsed = self.elapsed()
        if elapsed == 0.0:
            raise RuntimeError("PoolingTimer has never been started")
        return elapsed > self.timeout

class BlockConsoleHandler(logging.StreamHandler):

    default_level = logging.INFO
    pattern_indent = '+< '
    pattern_blocks = '|  '
    pattern_dedent = '+> '
    current_indent = ''

    def emit(self, record):
        cls = self.__class__
        if cls.is_debug():
            record.msg = '{}{}'.format(cls.current_indent, record.msg)
        logging.StreamHandler.emit(self, record)

        if cls.current_indent.endswith(cls.pattern_indent):
            cls.current_indent = (cls.current_indent[:-len(cls.pattern_indent)] + cls.pattern_blocks)
        elif cls.current_indent.endswith(cls.pattern_dedent):
            cls.current_indent = cls.current_indent[:-len(cls.pattern_dedent)]

    @classmethod 
    def is_debug(cls):
        """Return True if this handler is set to DEBUB level on the root logger.
        """
        for hdlr in logging.getLogger().handlers:
            if isinstance(hdlr, cls):
                return hdlr.level < logging.INFO 
        return False

    @classmethod
    def indent(cls):
        """Begin a new log block.
        """
        if cls.is_debug():
            cls.current_indent += cls.pattern_indent 

    @classmethod 
    def dedent(cls):
        """End the current log block.
        """
        if cls.is_debug():
            cls.current_indent = (cls.current_indent[:-len(cls.pattern_blocks)] + cls.pattern_dedent)

def configure_logging(level=logging.INFO, msgfmt=logging.BASIC_FORMAT, datefmt=None, filename=None):
    """Configure root logger for console printing.
    """
    root = logging.getLogger()

    if not root.handlers:
        # Set lower level to be sure that all handlers receive the logs
        root.setLevel(logging.DEBUG)

        if filename:
            # Create a file handler, all levels are logged
            filename = osp.abspath(osp.expanduser(filename))
            dirname = osp.dirname(filename)
            if not osp.isdir(dirname):
                os.makedirs(dirname)
            hdlr = logging.FileHandler(filename, mode='w')
            hdlr.setFormatter(logging.Formatter(msgfmt, datefmt))
            hdlr.setLevel(logging.DEBUG)
            root.addHandler(hdlr)

        # Create a console handler 
        hdlr = BlockConsoleHandler(sys.stdout)
        hdlr.setFormatter(logging.Formatter(msgfmt, datefmt))
        if level is not None:
            hdlr.setLevel(level)
            BlockConsoleHandler.default_level = level 
        root.addHandler(hdlr)


def set_logging_level(level=None):
    """Set/restore the log level of the console.
    :param level: level as defined in the logging package
    :type level: int
    """
    for hdlr in logging.getLogger().handlers:
        if isinstance(hdlr, BlockConsoleHandler):
            if level is None:
                # Restore the default level
                level = BlockConsoleHandler.default_level 
            hdlr.setLevel(level)

def get_logging_filename():
    """Return the absolute path to the logs filename if set.
    """
    for hdlr in logging.getLogger().handlers:
        if isinstance(hdlr, logging.FileHandler):
            return hdlr.baseFilename
    return None 

def get_crash_message():
    msg = "system='{}', node='{}', release='{}', version='{}', machine='{}', processor='{}'\n".format(*platform.uname())
    msg += " " + "*" * 83 + "\n"
    msg += " * " + "Oops! It seems that piticket has crashed".center(80) + "*\n"
    msg += " * " + "You can report an issue on https://github.com/piticket/piticket/issues/new".center(80) + "*\n"
    if get_logging_filename():
        msg += " * " + ("and post the file: {}".format(get_logging_filename()))
    msg += " " + "*" * 83
    return msg

def rename_gifs(fullpath_frames):
    """Rename all the gifs in a subdirectory
    """
    for frame in fullpath_frames:
        head, tail = osp.split(frame)
        name, ext = tail.split('.')
        if len(name) == 1:
            # test to know if it is a single digit
            os.rename(frame,osp.join(head,f'frame_0{name}.png'))
        if len(name) == 2:
            os.rename(frame,osp.join(head,f'frame_{name}.png'))


def multiline_text_to_surfaces(text, color, rect, align='center'):
    """Return a list of text surfaces(pygame.Surface) and corresponding positions
    The ``align```parameter can be one of:
        * top-left
        * top-center
        * top-right
        * center-left
        * center
        * center-right
        * bottom-left
        * bottom-center
        * bottom-right
    """
    surfaces = []
    # split text into list of strings using newline character
    lines = text.splitlines()
    # Return a SysFont object corresponding to the longest string
    font = get_pygame_font(max(lines, key=len),'nimbussansnarrow',rect.width,rect.height//len(lines))

    for i, line in enumerate(lines):
        surface = font.render(line, True, color)
        if align.endswith('left'):
            x = rect.left
        elif align.endswith('center'):
            x = rect.centerx - surface.get_rect().width//2
        elif align.endswith('right'):
            x = rect.right - surface.get_rect().width
        else:
            raise ValueError("Invalid horizontal argument '{}'".format(align))

        height = surface.get_rect().height
        if align.startswith('top'):
            y = rect.top + i*height
        elif align.startswith('center'):
            y = rect.centery - (len(lines)*height)//2 + height*i
        elif align.startswith('bottom'):
            y = rect.bottom - len(lines)*height + i*height
        else:
            raise ValueError("Invalid vertical argument '{}'".format(align))
   
        surfaces.append((surface,surface.get_rect(x=x,y=y)))

    return surfaces