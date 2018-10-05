#!/usr/bin/env python3

from . import widgets


class Window:
    """It creates a Window Object."""
    def __init__(self, width, height, fill=' '):
        self.content = widgets.create_matrix(
            x=width,
            y=height,
            fill=fill
            )

    def insert(self, matrix, x_vertex, y_vertex):
        """Each element of the matrix is inserted on the window."""
        # Variable to walk through the matrix (y value).
        y_index = 0
        while y_index < len(matrix) and y_vertex < len(self.content):
            # Variable to walk through the matrix (x value).
            x_index = 0
            x_vert = x_vertex
            while x_index < len(matrix[0]) and x_vert < len(self.content[0]):
                self.content[y_vertex][x_vert] = matrix[y_index][x_index]
                x_index += 1
                x_vert += 1
            y_index += 1
            y_vertex += 1

    def insert_point(self, point_character, x_coord, y_coord):
        """Each element of the matrix is inserted in the window."""
        self.content[y_coord][x_coord] = point_character

    def render(self):
        return '\n'.join([''.join(x) for x in self.content])
