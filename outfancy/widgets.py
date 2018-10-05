#!/usr/bin/env python3

import fcntl
import os
import struct
import termios

from datetime import datetime
from re import sub
from time import strptime


def actual_date():
    """This function return the actual date."""
    now = datetime.now()
    return f'{now.day}-{now.month}-{now.year}'


def actual_hour():
    """This function return the actual hour."""
    now = datetime.now()
    return f'{now.hour}:{now.minute}:{now.second}'


def compress_list(list_to_compress):
    """
    This function compress a list while maintaining order,
    I.e: [1, 6, 4] is converted in [0 ,2, 1].
    """
    # If list_to_compress is empty the same list is returned, because
    # is imposible to compress.
    if list_to_compress == []:
        return list_to_compress

    compressed_list = []
    # The list compressed_list is filled by a number of zeros that equals
    # the len of list_to_compress.
    for x in range(len(list_to_compress)):
        compressed_list.append(0)

    # Num used to fill compressed_list.
    num = 0
    # It walks the numbers from zero to maximum present in the list
    # list_to_compress.
    for x in range(max(list_to_compress) + 1):
        # If x (the minimal number in list_to_compress + x) is in
        # the list list_to_compress.
        number = min(list_to_compress) + x
        if number in list_to_compress:
            # num is added to compresed list in the index that is
            # occupied by the minimal number of list_to_compress.
            compressed_list[list_to_compress.index(number)] = num
            num += 1

    return compressed_list


def create_matrix(x, y, fill=''):
    """This function create a 2d matrix based on it dimensions."""
    return [[fill for p in range(x)] for p in range(y)]


def index_is_in_list(the_list, index):
    """This function check if an index is in the specified list."""
    return bool(0 <= index < len(the_list))


def is_complete_hour(text):
    """This function check if the input is a valid complete hour."""
    for fmt in ['%H:%M:%S', '%H:%M']:
        try:
            strptime(text, fmt)
            return True
        except ValueError:
            pass
    return False


def is_date(text):
    """
    This function check if the input is a valid date, format:
    "dd-mm-yyyy, dd-mm-yy, dd-mm-yyyy hh-mm-ss, dd-mm-yy hh-mm-ss"
    and: "d-m-yy, d-m-yyyy, h-m-s"
    """
    text = normalise_date(text)
    for fmt in ['%d-%m-%Y',
                '%d-%m-%y',
                '%d-%m-%Y %H-%M-%S',
                '%d-%m-%y %H-%M-%S'
                ]:
        try:
            strptime(text, fmt)
            return True
        except ValueError:
            pass

    return False


def printed_length(text):
    """This function measure the length of a printed string."""
    # It returns the length of the printed string
    return len(remove_colors(text))


def measure_screen(screen_x=None, screen_y=None):
    """
    Measure the screen dimensions (in characters),
    returning two values, X and Y.
    """
    env = os.environ

    def ioctl_GWINSZ(fd):
        try:
            cr = struct.unpack(
                'hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234')
                )
        except Exception:
            return
        return cr

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except Exception:
            pass

    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

    if screen_x is None:
        screen_x = int(cr[1])

    if screen_y is None:
        screen_y = int(cr[0])

    return screen_x, screen_y


def normalise_date(text):
    """This function normalize text, is useful to normalize dates."""
    text = text.replace(
        '/', '-').replace(
        ':', '-').replace(
        '.', '-').replace(
        '@', '-')
    return text


def remove_colors(text):
    """This function remove the ANSI color codes of a string."""
    return sub(
        r'\x1b\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?',
        '',
        text
        )
