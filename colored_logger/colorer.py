import logging
import textwrap
import itertools
import platform
import copy
import six
import colorama
import crayons


def getLogger(name):
    return logging.getLogger(name)

def customLogger(name, fn=None,
                 file_format='%(asctime)s - %(levelname)s - %(message)s',
                 mode='a', level='DEBUG', term_width=None):
    init()
    logger = logging.getLogger(name)
    if len(logger.handlers) == 0:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(MyFormatter(
            fmt="%(message)s", term_width=term_width))

        if fn is not None:
            fh = logging.FileHandler(fn, mode=mode)
            fh.setFormatter(logging.Formatter(file_format))
        logger.addHandler(stream_handler)
        logger.addHandler(fh)

    logger.setLevel(level)
    return logger


def setLevels(name=None, logger=None, level=None, file_level=None, stream_level=None):
    if (name is None) and (logger is None):
        return None
    elif name is not None:
        logger = logging.getLogger(name)

    if level is not None:
        logger.setLevel(level)
        return logger

    for handle in logger.handlers:
        if type(handle) == logging.StreamHandler:
            if stream_level is not None:
                handle.setLevel(stream_level)
        elif type(handle) == logging.FileHandler:
            if file_level is not None:
                handle.setLevel(file_level)
    return logger


def init():
    colorama.init()


'''
MyFormatter class
Adapted from: http://stackoverflow.com/questions/6847862/how-to-change-the-format-of-logged-messages-temporarily-in-python
              http://stackoverflow.com/questions/3096402/python-string-formatter-for-paragraphs
Authors: Vinay Sajip, unutbu

Using this formatter makes output look like:
TEXT TEXT TEXT TEXT [CRITICAL]
TEXT TEXT TEXT TEXT

Where width is dymanically taken from the terminal width.

A couple of nuanced points, white space at the beginning of the message is perserved throughout
the rest of the line wrapping.  For example logger.debug('\tThis is a cool message')
would result in

    This is a cool [  DEBUG]
    message

Tabs in the rest of the text are ignored (with one exception below). For example
logger.debug('\tThis is a cool \tmessage') is still just

    This is a cool [  DEBUG]
    message


New line commands are preserved, and the spacing for the first line is used
for line wrapping.  For example logger.debug('\tThis\nis\na\ncool\nmessage')

    This         [  DEBUG]
    is
    a
    cool
    message

Whitespace after the \n is preserved for the first wrapped line...non-ideal, but
its what happens.  For example logger.debug('\tThis is a cool message\n\tSecond cool message long')

    This is a cool [  DEBUG]
    message
        Second
    cool message
    long

It is not recommended to us \n with whitespace afterwards.
For example logger.debug('\tThis is a cool message\nSecond cool message long')

    This is a cool [  DEBUG]
    message
    Second cool
    message long

'''


class MyFormatter(logging.Formatter):

    def __init__(self, *args, term_width=None, **kwargs):
        super(MyFormatter, self).__init__(**kwargs)

        self.term_width = term_width

        # if term_width is None:
        #     self.term_width = getTerminalSize()[0]
        # else:
        #     self.term_width = term_width

    # This function overwrites logging.Formatter.format
    # We conver the msg into the overall format we want to see
    def format(self, record):

        if self.term_width is None:
            term_width = getTerminalSize()[0]
        else:
            term_width = self.term_width

        widths = [term_width - 12, 10]
        form = '{row[0]:<{width[0]}} {row[1]:<{width[1]}}'

        # Instead of formatting...rewrite message as desired here
        new_record = copy.deepcopy(record)

        # We need to consume the message here otherwise we get some wonky behavior
        total_message = new_record.getMessage()
        new_record.args = ()

        new_record.msg = self.createColumns(form, widths, [total_message], [
            "[%8s]" % new_record.levelname])

        new_record = self.addColor(new_record)
        # Return basic formatter
        return super(MyFormatter, self).format(new_record)

    @staticmethod
    def addColor(record):
        if record.levelno >= 50:
            record.msg = crayons.magenta(record.msg, bold=True)
        elif record.levelno >= 40:
            record.msg = crayons.red(record.msg, bold=True)
        elif record.levelno >= 30:
            record.msg = crayons.yellow(record.msg, bold=True)
        elif record.levelno >= 20:
            record.msg = crayons.green(record.msg, bold=False)
        elif record.levelno >= 10:
            record.msg = crayons.cyan(record.msg, bold=False)
        return record

    @staticmethod
    def createColumns(format_str, widths, *columns):
        '''
        format_str describes the format of the report.
        {row[i]} is replaced by data from the ith element of columns.
        widths is expected to be a list of integers.
        {width[i]} is replaced by the ith element of the list widths.
        All the power of Python's string format spec is available for you to use
        in format_str. You can use it to define fill characters, alignment, width, type, etc.
        formatter takes an arbitrary number of arguments.
        Every argument after format_str and widths should be a list of strings.
        Each list contains the data for one column of the report.
        formatter returns the report as one big string.
        '''
        result = []
        for row in zip(*columns):

            # Create a indents for each row...
            sub = []

            # Loop through
            for r in row:
                # Expand tabs to spaces to make our lives easier
                r = r.expandtabs()

                # Find the leading spaces and create indend character
                if r.find(" ") == 0:
                    i = 0
                    for letters in r:
                        if not letters == " ":
                            break
                        i += 1
                    sub.append(" " * i)
                else:
                    sub.append("")

            # Per text wrap perserving the \n should be done with splitlines
            row = [x.splitlines() for x in row]
            lines = []
            for elt, num, ind in zip(row, widths, sub):
                lt = []

                for i, e in enumerate(elt):

                    # Only set init_indent for non-first lines
                    if i == 0:
                        initial_indent = ''
                    else:
                        initial_indent = ind
                    lt.extend(textwrap.wrap(e, width=num,
                                            initial_indent=initial_indent, subsequent_indent=ind))
                lines.append(lt)

            if six.PY2:
                # pylint: disable=E1101
                for line in itertools.izip_longest(*lines, fillvalue=''):
                    result.append(format_str.format(width=widths, row=line))
            elif six.PY3:
                for line in itertools.zip_longest(*lines, fillvalue=''):
                    result.append(format_str.format(width=widths, row=line))
        return '\n'.join(result)


'''
Functions below: getTerminalSize
Author: http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
Author: Harco Kuppens
Downloaded 2/21/14
'''


def getTerminalSize():
    current_os = platform.system()
    tuple_xy = None
    if current_os == 'Windows':
        tuple_xy = _getTerminalSizeWindows()
        if tuple_xy is None:
            tuple_xy = _getTerminalSizeTput()
            # needed for window's python in cygwin's xterm!
    if current_os == 'Linux' or current_os == 'Darwin' or current_os.startswith('CYGWIN'):
        tuple_xy = _getTerminalSizeLinux()
    if tuple_xy is None:
        print("default")
        tuple_xy = (80, 25)      # default value
    return tuple_xy


def _getTerminalSizeWindows():
    res = None
    try:
        from ctypes import windll, create_string_buffer

        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12

        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
    except:
        return None
    if res:
        import struct
        (bufx, bufy, curx, cury, wattr,
         left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
        sizex = right - left + 1
        sizey = bottom - top + 1
        return sizex, sizey
    else:
        return None


def _getTerminalSizeTput():
    # get terminal width
    # src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
    try:
        import subprocess
        proc = subprocess.Popen(
            ["tput", "cols"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output = proc.communicate(input=None)
        cols = int(output[0])
        proc = subprocess.Popen(
            ["tput", "lines"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output = proc.communicate(input=None)
        rows = int(output[0])
        return (cols, rows)
    except:
        return None


def _getTerminalSizeLinux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            import struct
            import os
            cr = struct.unpack('hh', fcntl.ioctl(
                fd, termios.TIOCGWINSZ, '1234'))
        except:
            return None
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (env['LINES'], env['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])
