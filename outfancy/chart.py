#!/usr/bin/env python3

from . import widgets
from .window import Window

from math import nan


class LineChart:
    """Line Charts in terminal."""
    def __init__(self):
        self.dataset_space = []
        self.x_min = 0
        self.x_max = 0
        self.y_min = 0
        self.y_max = 0

    def get_list_of_elements(self, table):
        # It return a list of x and a list of y values.
        return [x[0] for x in table], [x[1] for x in table]

    def clear(self):
        self.dataset_space = []

    def plot(self, dataset):
        # The data is checked.
        integrity, reason = self.check_data_integrity(dataset)
        if not integrity:
            message = '--- Plot > Line > Input data is invalid. ---\n'
            message += f'Reason: {reason}'
            return message

        x_values, y_values = self.get_list_of_elements(dataset)

        # The maximum and minimum values are calculated.
        if min(x_values) < self.x_min:
            self.x_min = min(x_values)
        if max(x_values) > self.x_max:
            self.x_max = max(x_values)

        if min(y_values) < self.y_min:
            self.y_min = min(y_values)
        if max(y_values) > self.y_max:
            self.y_max = max(y_values)

        self.dataset_space.append([x_values, y_values])

    def get_char_slope(self, slope, color, color_number):
        """We generate a point character to plot based on slope."""
        if slope is nan:
            return '|'
        if slope > 2 or slope < -2:
            point_character = '|'
        elif slope > .7:
            point_character = '/'
        elif slope < -.7:
            point_character = '\\'
        else:
            point_character = '—'

        if color:
            point_character = f'\x1b[1;{color_number}m'\
                f'{point_character}\x1b[0;99m'
        return point_character

    def y_interpolate(self, interpolated_points, point_character):
        """|
        i = 0
        while i < len(interpolated_points) - 1:
            actual_point = interpolated_points[i]
            next_point = interpolated_points[i + 1]
            # If y distance between
            # actual and next point is greater than 1.
            y_interpolated_points = []
            c = 0
            c1 = next_point[2] - actual_point[2] > 1
            c2 = next_point[2] - actual_point[2] < -1
            if c1 or c2:
                if c1:
                    c += 1
                elif c2:
                    c -= 1
                x_actual = actual_point[1]
                y_actual = actual_point[2]

                new_point = [point_character, x_actual, y_actual + c]
                y_interpolated_points.append(new_point)

                interpolated_points = interpolated_points[
                    :i
                    ] + y_interpolated_points\
                    + interpolated_points[i:]
            i += len(y_interpolated_points) + 1
        """
        return interpolated_points

    def render(
        self,
        plot_name='',
        point_list=None,
        left_margin_width=8,
        margin_down_height=8,
        margin_top_height=3,
        color=False,
        background_point='·',
        color_number_list=None,
        interpolation=True,
        slope_based_characters=True,
        remove_unnecesary_points_before_plotting=True
            ):
        ###########################
        # --- PRE-RENDER AREA --- #
        ###########################
        # --- The screen measures are obtained --- #
        screen_x, screen_y = widgets.measure_screen()

        # --- Values of chart_window are calculated. ---#
        chart_window_x = screen_x - left_margin_width
        chart_window_y = screen_y - margin_down_height - margin_top_height

        chart_window_x_range = abs(self.x_max - self.x_min)
        chart_window_y_range = abs(self.y_max - self.y_min)

        if chart_window_x - 1 != 0:
            x_points_per_x_pixel = chart_window_x_range / (chart_window_x - 1)
        else:
            x_points_per_x_pixel = 1

        if chart_window_y - 1 != 0:
            y_points_per_y_pixel = chart_window_y_range / (chart_window_y - 1)
        else:
            x_points_per_x_pixel = 1

        print(x_points_per_x_pixel)
        print(y_points_per_y_pixel)
        #######################
        # --- RENDER AREA --- #
        #######################

        if not point_list:
            point_list = list('xoabcdefghijklmnpqrstuvwyz')

        if not color_number_list:
            color_number_list = [33,
                                 91,
                                 32,
                                 31,
                                 34,
                                 35,
                                 36,
                                 37,
                                 90,
                                 92,
                                 93,
                                 94,
                                 95,
                                 96,
                                 97
                                 ]

        # An empty matrix is created.
        if color:
            background_point = f'\x1b[1;90m{background_point}\x1b[0;99m'

        chart_window = Window(
            width=chart_window_x,
            height=chart_window_y,
            fill=background_point
            )

        def add_point(point_character, x, y):
            if chart_window_y - y - 1 > 0:
                chart_window.insert_point(
                    point_character=point_character,
                    x_coord=x,
                    y_coord=chart_window_y - y - 1
                    )

        # If the dataset is not empty.
        if len(self.dataset_space) > 0:
            point_counter = 0
            color_number_index = 0

            # We want to plot each dataset.
            for dataset in self.dataset_space:
                # We select a color to plot the line of this dataset.
                color_number = color_number_list[color_number_index]

                if color:
                    point_character = f'\x1b[1;{color_number}m'\
                                      f'{point_list[point_counter]}\x1b[0;99m'
                else:
                    point_character = point_list[point_counter]

                c2 = len(dataset[0]) > screen_x - left_margin_width * 2
                if remove_unnecesary_points_before_plotting and c2:
                    step = round(
                        len(dataset[0]) / (screen_x - left_margin_width) / 2
                        )

                    if step != 0:
                        dataset[0] = [
                            dataset[0][i] for i in range(
                                0, len(dataset[0]), step
                                )
                            ]
                        dataset[1] = [
                            dataset[1][i] for i in range(
                                0, len(dataset[1]), step
                                )
                            ]

                last_x = None
                chart_screen_points = []
                # For each point in dataset.
                for element in range(len(dataset[0])):
                    x = round(
                        (
                            dataset[0][element] - self.x_min
                            ) / x_points_per_x_pixel
                        )
                    if x != last_x:
                        # x is scaled to the size of the table.
                        y = round(
                            (
                                dataset[1][element] - self.y_min
                                ) / y_points_per_y_pixel
                            )
                        chart_screen_points.append([point_character, x, y])
                        last_x = x

                # We apply linear interpolation.
                if interpolation and len(chart_screen_points) > 1:
                    # We use point index to walk through chart_screen_points.
                    point_index = 0
                    # We start our walk.
                    while point_index < len(chart_screen_points):
                        # We mark the actual point as the point_index we are.
                        actual_point = chart_screen_points[point_index]

                        # If next point index exists, we assign it to
                        # next_point_index.
                        if widgets.index_is_in_list(
                            the_list=chart_screen_points,
                            index=point_index + 1
                                ):

                            next_point = chart_screen_points[point_index + 1]
                            # If x distance between
                            # actual and next point is greater than 1.
                            if next_point[1] != actual_point[1] - 1:
                                x_actual = actual_point[1]
                                y_actual = actual_point[2]
                                x_next = next_point[1]
                                y_next = next_point[2]

                                y_distance = y_next - y_actual
                                x_distance = x_next - x_actual

                                # X_distance is always greater than zero
                                # because we are filling holes.
                                slope = y_distance / x_distance

                                interpolated_points = []
                                for i in range(x_next - x_actual):
                                    new_point_x = x_actual + i
                                    new_point_y = y_actual + round(slope * i)

                                    new_point = [
                                        point_character,
                                        new_point_x,
                                        new_point_y
                                        ]

                                    interpolated_points.append(new_point)

                                # We check for vertical characters.
                                interpolated_points = self.y_interpolate(
                                    interpolated_points=interpolated_points,
                                    point_character=point_character
                                    )

                                chart_screen_points = chart_screen_points[
                                    :point_index
                                    ] + interpolated_points\
                                      + chart_screen_points[point_index:]

                        point_index += len(interpolated_points) + 1

                    """
                    # We check for vertical characters.
                    chart_screen_points = self.y_interpolate(
                        interpolated_points=chart_screen_points,
                        point_character=point_character
                        )
                    """

                # Here we apply slope based characters.
                if slope_based_characters and len(chart_screen_points) > 1:
                    for point_index in range(len(chart_screen_points) - 1):
                        actual_point = chart_screen_points[point_index]
                        next_point = chart_screen_points[point_index + 1]

                        x_actual = actual_point[1]
                        y_actual = actual_point[2]
                        x_next = next_point[1]
                        y_next = next_point[2]

                        y_distance = y_next - y_actual
                        x_distance = x_next - x_actual

                        if x_distance != 0:
                            slope = y_distance / x_distance
                        else:
                            slope = nan

                        point_character = self.get_char_slope(
                            slope=slope,
                            color=color,
                            color_number=color_number
                            )

                        actual_point[0] = point_character

                    # We apply the slope character to last point in chart.
                    chart_screen_points[point_index + 1][0] = point_character

                # We add points to chart_window.
                for point in chart_screen_points:
                    add_point(
                        point_character=point[0],
                        x=point[1],
                        y=point[2]
                        )

                if color_number_index != len(color_number_list) - 1:
                    color_number_index += 1
                else:
                    color_number_index = 0

                if point_counter != len(point_list) - 1:
                    point_counter += 1
                else:
                    point_counter = 0

        # --- Margins are created. ---
        top_margin = self.create_top_margin(
            height=margin_top_height,
            width=screen_x,
            tag=plot_name
            )

        left_margin = self.create_left_margin(
            height=chart_window_y,
            width=left_margin_width,
            min_value=self.y_min,
            max_value=self.y_max
            )

        down_margin = self.create_down_margin(
            height=margin_down_height,
            width=chart_window_x,
            min_value=self.x_min,
            max_value=self.x_max
            )

        margin_down_y_vertex = screen_y - margin_down_height

        # --- Window is composed. ---
        window = Window(
            width=screen_x,
            height=screen_y,
            fill=' '
            )

        window.insert(
            matrix=top_margin,
            x_vertex=0,
            y_vertex=0
            )

        window.insert(
            matrix=left_margin,
            x_vertex=0,
            y_vertex=margin_top_height
            )

        if margin_down_y_vertex > 0:
            window.insert(
                matrix=down_margin,
                x_vertex=left_margin_width,
                y_vertex=margin_down_y_vertex
                )

            if left_margin_width - 2 > 0:
                window.insert(
                    matrix=['└—'],
                    x_vertex=left_margin_width - 2,
                    y_vertex=margin_down_y_vertex
                    )

        window.insert(
            matrix=chart_window.content,
            x_vertex=left_margin_width,
            y_vertex=margin_top_height
            )

        return window.render()

    def create_top_margin(self, height, width, tag=''):
        # A matrix is created.
        fill = ' '
        if height > 1:
            top_margin = [fill * width for line in range(height)]
            if len(tag) < width:
                line_tag = tag.center(width, fill)
            else:
                line_tag = tag[:width]
            top_margin[int(height / 2)] = line_tag
        return top_margin

    def create_left_margin(
        self,
        height,
        width,
        min_value,
        max_value,
        separator='┼'
            ):

        # A matrix is created.
        left_margin = widgets.create_matrix(x=width, y=height)

        # This value is created to register remaining space.
        free_width = width

        # The separator is inserted in each line.
        for y in range(height):
            left_margin[y][free_width - 1] = separator

        free_width -= 2

        # Each value is inserted in each line.
        y_values = [
                str(
                    (
                        (max_value - min_value) / (height - 1)
                        ) * y + min_value
                    ) for y in range(height)
                ]

        y_values.reverse()
        for y in range(height):
            if len(y_values[y]) > free_width:
                y_values[y] = y_values[y][:free_width]
            else:
                y_values[y] = f'{y_values[y]}'\
                              f'{" " * (free_width - len(y_values[y]))}'

            for x in range(0, free_width):
                left_margin[y][x] = y_values[y][x]

        return left_margin

    def create_down_margin(
        self,
        height,
        width,
        min_value,
        max_value,
        separator1='┼',
        separator2='–'
            ):

        # A matrix is created.
        down_margin = widgets.create_matrix(x=width, y=height)

        # This value is created to register remaining space.
        free_height = height

        down_margin[0] = [
            (separator1 if x % 2 == 0 else separator2) for x in range(width)
            ]
        free_height -= 1

        values = [
            str(
                ((max_value - min_value) / (width - 1)) * x + min_value
                ) for x in range(width)
            ]

        for x in range(width):
            if len(values[x]) > free_height:
                values[x] = values[x][:free_height]
            else:
                values[x] = f'{values[x]}'\
                            f'{"0" * (free_height - len(values[x]))}'

            values[x] = values[x].replace('.', '·')
            for y in range(height - free_height, height):
                new_y = y - (height - free_height)
                down_margin[y][x] = (values[x][new_y] if x % 2 == 0 else ' ')
        return down_margin

    def check_data_integrity(self, dataset):
        """This function check the data integrity."""
        integrity = True
        reason = None

        # The table data is checked.
        if isinstance(dataset, list):
            if len(dataset) == 0:
                integrity = False
                reason = 'The dataset have not elements.'
            else:
                # The rows of table are checked.
                for ordered_pair in dataset:
                    is_tuple = isinstance(ordered_pair, tuple)
                    is_list = isinstance(ordered_pair, list)
                    if is_tuple or is_list:
                        if len(ordered_pair) == 2:
                            # For each variable of ordered_pair.
                            for element in ordered_pair:
                                # The element is valid if
                                # his type is an int, float or None.
                                integrity = False
                                reason = 'An element of an ordered_pair is '\
                                    'not an int, float or None.'
                                is_int = isinstance(element, int)
                                is_float = isinstance(element, float)
                                if is_int or is_float or element is None:
                                    integrity = True
                                    reason = None
                        else:
                            integrity = False
                            reason = 'An element is not an ordered pair.'
                    else:
                        integrity = False
                        reason = 'An element is not an ordered pair.'
        else:
            integrity = False
            reason = 'The input is not a list.'

        return integrity, reason
