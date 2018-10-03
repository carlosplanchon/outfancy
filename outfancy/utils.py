#!/usr/bin/env python3


def create_matrix(x, y, fill=''):
    """This function create a 2d matrix based on it dimensions."""
    return [[fill for p in range(x)] for p in range(y)]
