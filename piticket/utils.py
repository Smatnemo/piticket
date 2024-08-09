import os
import sys 
import logging
import platform


import os.path as osp


LOGGER = logging.getLogger('piticket')


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
