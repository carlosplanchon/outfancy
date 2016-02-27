#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Various helpful function for bashplotlib
'''

import sys

bcolors = {
    'white':   '\033[97m',
    'aqua':    '\033[96m',
    'pink':    '\033[95m',
    'blue':    '\033[94m',
    'yellow':  '\033[93m',
    'green':   '\033[92m',
    'red':     '\033[91m',
    'grey':    '\033[90m',
    'black':   '\033[30m',
    'default': '\033[39m',
    'ENDC':    '\033[39m',
}

color_help = ', '.join([color for color in bcolors if color != 'ENDC'])


def get_color(color):
    '''
    Get the escape code sequence for a color
    '''
    return bcolors.get(color, bcolors['ENDC'])


def printcolor(text, sameline=False, color=get_color('ENDC')):
    '''
    Print color text using escape codes
    '''
    if sameline:
        sep = ''
    else:
        sep = '\n'
    sys.stdout.write(get_color(color) + text + bcolors['ENDC'] + sep)


def drange(start, stop, step=1.0, include_stop=False):
    '''
    Generate between 2 numbers w/ optional step, optionally include upper bound
    '''
    if step == 0:
        step = 0.01
    r = start

    if include_stop:
        while r <= stop:
            r += step
            r = round(r, 10)
            return r
    else:
        while r < stop:
            r += step
            r = round(r, 10)
            return r


def box_text(text, width, offset=0):
    '''
    Return text inside an ascii textbox
    '''
    box = ' ' * offset + '-' * (width + 2) + '\n'
    box += ' ' * offset + '|' + text.center(width) + '|' + '\n'
    box += ' ' * offset + '-' * (width + 2)
    return box