#!/usr/bin/env python3

import utils


class Window:
    """It creates a Window Object."""
    def __init__(self, width, heigth, fill=' '):
        self.content = utils.create_matrix(width, heigth, fill)

    def insert(self, matrix, x_vertex, y_vertex):
        """Each element of the matrix is inserted in the window."""
        # We want to work in a matrix and a screen with elements.
        if len(matrix) > 0 and len(self.content) > 0:
            # Variable to control where we want to insert each point (y value).
            y_to_insert = y_vertex
            # Variable to walk through the matrix (y value).
            y_index = 0
            while y_to_insert < len(self.content):
                # Variable to control where we want to insert each point
                # (x value).
                x_to_insert = x_vertex
                # Variable to walk through the matrix (x value).
                x_index = 0
                while x_to_insert < len(self.content[0]):

                    self.content[
                        y_to_insert][x_to_insert] = matrix[y_index][x_index]

                    x_to_insert += 1
                    x_index += 1

                y_to_insert += 1
                y_index += 1

    def insert_point(self, point, x_coord, y_coord):
        """Each element of the matrix is inserted in the window."""
        self.content[y_coord][x_coord] = point

    def render(self):
        return '\n'.join([''.join(x) for x in self.content])
