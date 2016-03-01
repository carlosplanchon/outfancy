#!/usr/bin/python3
# -*- coding: utf-8 -*-

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
#    normalise_text(text)                 - This function normalise dates.                          #
#    is_date(text)                        - Check if the input is a valid date.                     #
#    is_complete_hour(text)               - Check if the input is a valid hour.                     #
#    actual_date()                        - Returns the actual date.                                #
#    actual_hour()                        - Returns the actual hour.                                #
#    measure_screen()                     - Measures characters that can fit on the screen.         #
#    compress_list(list_to_compress)      - Compress a list, I.e: [1,6,4] is converted in [0,2,1].  #
#    index_is_in_list(index, the_list)    - Check if an index is in the specified list.             #
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

# This function do the start checking.
def start_check():
    if not os.path.exists(outfancy_temp_files):
        os.mkdir(outfancy_temp_files)
    if not os.path.exists(outfancy_temp_files + log_file):
        os.system('touch ' + outfancy_temp_files + log_file)

# This function join a list using spaces.
def list_join(the_list):
    return ' '.join(the_list)

# This function write a file
def write_file(name_file, string):
    file = open(name_file, 'w')
    file.write(string)
    file.close()

# This function read a file.
def read_file(name_file):
    file = open(name_file, 'r')
    content = file.read()
    file.close()
    return content

# This function writes the log.
def write_log(text):
    log = read_file(log_file)
    write_file(log_file, log + '\n' + text)

# This function normalize text, is useful to normalize dates.
def normalise_text(text):
    text = text.replace('/','-')
    text = text.replace(':','-')
    text = text.replace('.','-')
    text = text.replace('@','-')
    return text

# This function check if the input is a valid date.
def is_date(text):
    text = normalise_text(text)
    for fmt in ['%d-%m-%Y', '%d-%m-%y', '%d-%m-%Y %H-%M-%S', '%d-%m-%y %H-%M-%S']:
        try:
            strptime(text, fmt)
            return True    
        except ValueError:
            pass
    return False

# This function check if the input is a valid hour.
def is_complete_hour(text):
    for fmt in ['%H:%M:%S', '%H:%M']:
        try:
            strptime(text, fmt)
            return True    
        except ValueError:
            pass
    return False

# This function return the actual date.
def actual_date():
    actual_date = datetime.now()
    return str(actual_date.day) + '-' + str(actual_date.month) + '-' + str(actual_date.year)

# This function return the actual hour.
def actual_hour():
    actual_hour = datetime.now()
    return str(actual_hour.hour) + ':' + str(actual_hour.minute) + ':' + str(actual_hour.second)

# Measure the screen dimensions (in characters), returning two values, X and Y.
def measure_screen():
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

# This function compress a list, I.e: [1,6,4] is converted in [0,2,1].
def compress_list(list_to_compress):
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

# This function check if an index is in the specified list.
def index_is_in_list(index, the_list):
    if index < len(the_list) and index >= 0:
        return True
    else:
        return False
