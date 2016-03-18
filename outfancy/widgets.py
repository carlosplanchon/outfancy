#!/usr/bin/env python3

#####################################################################################################
#                                                                                                   #
#    WIDGETS MODULE                                                                                 #
#                                                                                                   #
#    This module have little but important widgets that are useful to other modules.                #
#                                                                                                   #
#    MODULE FUNCTION INDEX                                                                          #
#---------------------------------------------------------------------------------------------------#
#                                                                                                   #
#    start_check()                        - Do the start check.                                     #
#    list_join(lista_comando)             - Join a list using spaces.                               #
#    write_file(name_file, cadena)        - Write a text in a file.                                 #
#    read_file(name_file)                 - Read a file.                                            #
#    write_log(text)                      - This function writes the log.                           #
#    normalise_date(text)                 - This function normalise dates.                          #
#    is_date(text)                        - Check if the input is a valid date.                     #
#    is_complete_hour(text)               - Check if the input is a valid hour.                     #
#    actual_date()                        - Returns the actual date.                                #
#    actual_hour()                        - Returns the actual hour.                                #
#    measure_screen()                     - Measures characters that can fit on the screen.         #
#    compress_list(list_to_compress)      - Compress a list, I.e: [1,6,4] is converted in [0,2,1].  #
#    index_is_in_list(index, the_list)    - Check if an index is in the specified list.             #
#    remove_colors(string)                - This function remove the color codes of a string.       #
#    printed_length(string)               - Measure the length of a printed string.                 #
#                                                                                                   #
#####################################################################################################

import os
import fcntl
import termios
import struct
import string
from time import strptime
from datetime import datetime

# Log file location.
outfancy_temp_files = '/tmp/outfancy/'
log_file = 'log.log'


def start_check():
    """This function do the start checking."""
    if not os.path.exists(outfancy_temp_files):
        os.mkdir(outfancy_temp_files)
    if not os.path.exists(outfancy_temp_files + log_file):
        os.system('touch ' + outfancy_temp_files + log_file)


def list_join(the_list):
    """This function join a list using spaces."""
    return ' '.join(the_list)


def write_file(name_file, string):
    """This function write a file."""
    with open(name_file, 'w') as file:
        file.write(string)


def read_file(name_file):
    """This function read a file."""
    with open(name_file, 'r') as file:
        return file.read()


def write_log(text):
    """This function writes the log."""
    write_file(read_file(log_file), log + '\n' + text)


def normalise_date(text):
    """This function normalize text, is useful to normalize dates."""
    text = text.replace('/', '-')
    text = text.replace(':', '-')
    text = text.replace('.', '-')
    text = text.replace('@', '-')
    return text


def is_date(text):
    """This function check if the input is a valid date, format:
        format: "dd-mm-yyyy, dd-mm-yy, dd-mm-yyyy hh-mm-ss, dd-mm-yy hh-mm-ss"
        and: "d-m-yy, d-m-yyyy, h-m-s"
    """
    text = normalise_date(text)
    for fmt in ['%d-%m-%Y', '%d-%m-%y', '%d-%m-%Y %H-%M-%S', '%d-%m-%y %H-%M-%S']:
        try:
            strptime(text, fmt)
            return True    
        except ValueError:
            pass
    return False


def is_complete_hour(text):
    """This function check if the input is a valid complete hour."""
    for fmt in ['%H:%M:%S', '%H:%M']:
        try:
            strptime(text, fmt)
            return True    
        except ValueError:
            pass
    return False


def actual_date():
    """This function return the actual date."""
    actual_date = datetime.now()
    return str(actual_date.day) + '-' + str(actual_date.month) + '-' + str(actual_date.year)


def actual_hour():
    """This function return the actual hour."""
    actual_hour = datetime.now()
    return str(actual_hour.hour) + ':' + str(actual_hour.minute) + ':' + str(actual_hour.second)


def measure_screen():
    """Measure the screen dimensions (in characters), returning two values, X and Y."""
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return
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
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
    return int(cr[1]), int(cr[0])


def compress_list(list_to_compress):
    """This function compress a list, I.e: [1,6,4] is converted in [0,2,1]."""
    # If list_to_compress is empty the same list is returned, becose is imposible to compress.
    if list_to_compress == []:
        return list_to_compress

    compressed_list = []
    # The list compressed_list is filled by a number of zeros that equals the len of list_to_compress.
    for x in range(len(list_to_compress)):
        compressed_list.append(0)

    # Num used to fill compressed_list.
    num = 0
    # It walks the numbers from zero to maxima present in the list list_to_compress.
    for x in range(max(list_to_compress) + 1):
        # If x (the minimal number in list_to_compress + x) is in the list list_to_compress.
        number = min(list_to_compress) + x
        if number in list_to_compress:
            # num is added to compresed list in the index that is occupied by the minimal number of list_to_compress.
            compressed_list[list_to_compress.index(number)] = num
            num += 1

    return compressed_list


def index_is_in_list(index, the_list):
    """This function check if an index is in the specified list."""
    if index < len(the_list) and index >= 0:
        return True
    else:
        return False


def remove_colors(string):
    """This function remove the color codes of a string."""
    color_list = ['\x1b[0;30m', '\x1b[0;31m', '\x1b[0;32m', '\x1b[0;33m', '\x1b[0;34m', '\x1b[0;35m', '\x1b[0;36m', '\x1b[0;37m', '\x1b[0;39m', '\x1b[0;40m', '\x1b[0;41m', '\x1b[0;42m', '\x1b[0;43m', '\x1b[0;44m', '\x1b[0;45m', '\x1b[0;46m', '\x1b[0;47m', '\x1b[0;49m', '\x1b[0;90m', '\x1b[0;91m', '\x1b[0;92m', '\x1b[0;93m', '\x1b[0;94m', '\x1b[0;95m', '\x1b[0;96m', '\x1b[0;97m', '\x1b[0;99m', '\x1b[0;100m', '\x1b[0;101m', '\x1b[0;102m', '\x1b[0;103m', '\x1b[0;104m', '\x1b[0;105m', '\x1b[0;106m', '\x1b[0;107m', '\x1b[0;109m', '\x1b[1;30m', '\x1b[1;31m', '\x1b[1;32m', '\x1b[1;33m', '\x1b[1;34m', '\x1b[1;35m', '\x1b[1;36m', '\x1b[1;37m', '\x1b[1;39m', '\x1b[1;40m', '\x1b[1;41m', '\x1b[1;42m', '\x1b[1;43m', '\x1b[1;44m', '\x1b[1;45m', '\x1b[1;46m', '\x1b[1;47m', '\x1b[1;49m', '\x1b[1;90m', '\x1b[1;91m', '\x1b[1;92m', '\x1b[1;93m', '\x1b[1;94m', '\x1b[1;95m', '\x1b[1;96m', '\x1b[1;97m', '\x1b[1;99m', '\x1b[1;100m', '\x1b[1;101m', '\x1b[1;102m', '\x1b[1;103m', '\x1b[1;104m', '\x1b[1;105m', '\x1b[1;106m', '\x1b[1;107m', '\x1b[1;109m']
    for x in color_list:
        string = string.replace(x, '')
        return string


def printed_length(string):
    """This function measure the length of a printed string."""
    # It returns the length of the printed string
    return len(remove_colors(string))


"""
--- IF ANYBODY CAN DEVELOP THIS FUNCTION USING REGEX, WELCOME IS ---

import re


def remove_colors(string):
    '''This function remove the color codes of a string.'''
    # strip_ANSI_pat remove the invisible characters using regular expresions.
    strip_ANSI_pat = re.compile(r'''
        \x1b     # literal ESC
        \[       # literal [
        [;\d]*   # zero or more digits or semicolons
        [A-Za-z] # a letter
        ''', re.VERBOSE).sub

    # It returns the string without special characters.
    return strip_ANSI_pat('', string)
"""
