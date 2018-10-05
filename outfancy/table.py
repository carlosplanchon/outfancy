#!/usr/bin/env python3

import logging

from . import widgets

from .example_dataset import dataset

from string import ascii_letters


logging.basicConfig(
    # filename='/tmp/outfancy/latest.log',
    level=logging.CRITICAL,
    format='%(asctime)s:%(levelname)s: %(message)s'
    )


class Table:
    """
    Table allow to render a table with nice format, the data input have to
    accomplish the format [(1, 'foo'), (2, 'bar')].
    """
    def __init__(self):
        #################################
        # --- Rendering parameters. --- #
        #################################
        # Check_data specify if the input data have to be checked or not.
        self.check_data = False
        # Check_data_size specify if the size of table data have
        # to be checked or not.
        self.check_table_size = False
        # Corrector = Indicates the correction value to be applied
        # to the x axis (margin of whitespaces at right of the screen).
        self.corrector = -2
        # Maximum heigth that a tuple can have in screen.
        self.max_heigth_of_a_tuple = 20
        # Analysis threshold (in rows) at the moment of analyze data_type_list.
        self.analyze_threshold = 10
        # The minimum width that a column need to be showed in screen.
        self.show_width_threshold = 5
        # row_separator_before_table allow to deactivate
        # the row_separator before table.
        self.row_separator_before_table = True

        # ###################### #
        # -v- IN DEVELOPMENT -v- #
        # ###################### #
        # row_separator_before_labels allow to enable the row_separator
        # before labels.
        # self.row_separator_before_labels = False
        # separator_before_table allow to enable the separator before table.
        # self.separator_before_table = False
        # separator_after_table allow to enable the separator after table.
        # self.separator_after_table = False
        # The string used for the separator intersection.
        # self.intersection_separator = None
        # The style used in the table.
        # self.style = None

        """
        The style have to be applied with a method like.
        self.set_style('grid')

        The parameters of the table have to be configurated according
        # with the style selected.

        I want to find better ideas at the moment of application of
        the separators.
        The variables:  row_separator_before_labels,
                        self.row_separator_before_labels,
                        self.separator_before_table,
                        self.separator_after_table
            are really stupid variables, another way to apply the separators
            maybe will be a list like
            row_separator_apply = [False, True, True, True, True, True, False]
            row_separator_apply[0] == False, then separator IS NOT applied
            before labels.
            row_separator_apply[1] == True, then separator IS applied
            after labels.

            The same idea can be applied for the separators (between columns).
            This allow to do grids easily.
        """

        #                        #
        # -^- IN DEVELOPMENT -^- #
        ##########################

        ####################
        # --- Measures --- #
        ####################
        # The maximum number of rows that a table can have (-1 = unlimited).
        self.maximum_number_of_rows = -1

        ###################
        # --- Options --- #
        ###################
        # Toggle the label showing above the table.
        self.show_labels = True

        """
        --- configuration parameters ---
        > check_data_type_list_integrity >
          data type recognizer.
        """

        # Default values by default works well, it is not recommended
        # its modification.

        # Number of letters required to be considered desc
        # (below this value is assumed that the type is a name).
        self.chk_dlti_num_letters_in_field = 15
        # Percentage of letters required to be considered a name.
        self.chk_dlti_pecentage_letters_in_field = 90

        # Percentage of type 'date' to be considered date.
        self.chk_dtli_date = 70
        # Percentage of type 'time' to be considered time.
        self.chk_dtli_time = 70
        # Percentage of type 'id' to be considered id.
        self.chk_dtli_id = 50
        # Percentage of type 'value' to be considered value.
        self.chk_dlti_value = 100
        # Percentage of type 'name' to be considered name.
        self.chk_dlti_name = 60
        # Percentage of type 'desc' to be considered desc.
        self.chk_dlti_desc = 60

    def set_check_data(self, x=False):
        """
        If check_data == True the dataset input will be checked.
        If you don't trust the data source, enable the data checking.
        """
        self.check_data = x

    def set_check_table_size(self, x=False):
        """
        If check_table_size == True, the measures of the table will be
        checked. If you don't trust the data source, enable the data measuring.
        """
        self.check_table_size = x

    def set_corrector(self, x=-2):
        """
        The corrector is a value that will be added to screen_x length,
        is -2 by default.
        """
        self.corrector = x

    def set_max_heigth_of_a_tuple(self, x=20):
        """This allow to modify the max heigth that a tuple can have."""
        self.max_heigth_of_a_tuple = x

    def set_analyze_threshold(self, x=10):
        """
        The analyze threshold is the number of tuples that will be analyzed
        in check_data_type_list_integrity.
        """
        self.analyze_threshold = x

    def set_show_width_threshold(self, x=True):
        """
        This function show the width threshold, below the width thresold,
        a column will not be showed.
        """
        self.show_width_threshold = x

    def set_show_labels(self, x=True):
        """This function enable the labels showing."""
        self.show_labels = x

    def set_maximum_number_of_rows(self, x=-1):
        """
        This function allow to modify the maximum number of rows
        outfancy can show, by default is infinite (-1).
        """
        self.maximum_number_of_rows = x

    def set_row_separator_before_table(self, x=True):
        """
        Row_separator_before_table allow to enable or
        disable the separator before the table.
        """
        self.row_separator_before_table = x

    def show_check_data(self):
        """It shows the value of the variable check_data."""
        print(self.check_data)

    def show_check_table_size(self):
        """It shows the value of the variable check_table_size."""
        print(self.check_table_size)

    def show_corrector(self):
        """It shows the value of the corrector."""
        print(self.corrector)

    def show_max_heigth_of_a_tuple(self):
        """It shows the value of the variable max_heigth_of_a_tuple."""
        print(self.max_heigth_of_a_tuple)

    def show_analyze_threshold(self):
        """It shows the value of the variable analyze_threshold."""
        print(self.analyze_threshold)

    def show_show_width_threshold(self):
        """It shows the value of the variable show_width_threshold."""
        print(self.show_width_threshold)

    def show_show_labels(self):
        """It shows the value of the variable show_labels."""
        print(self.show_labels)

    def show_maximum_number_of_rows(self):
        """It shows the value of the variable maximum_number_of_rows."""
        print(self.maximum_number_of_rows)

    def show_row_separator_before_table(self):
        """It shows the value of the variable row_separator_before_table."""
        print(self.row_separator_before_table)

    def render(
        self,
        data=None,
        separator=None,
        label_list=None,
        order=None,
        data_type_list=None,
        priority_list=None,
        width=None,
        row_separator=None,
        page=None,
        screen_x=None,
        screen_y=None
            ):

        """
        Render receives six (6) parameters, and is responsible for the
        rendering of data on a table in an organized way.

        Parameters:
        data: It have to be specified in the next format:
            [(1, 'Amelia', 'Lawyer'), (2, 'Camille', 'Chef')].
        separator: It allow to modify the string that separate the columns,
            by default is a white space " ".
        label_list: Allows to modify the label list that is
            showed above renderized table.
            If it is not provided, the program will try to find out what
                label will have each column.
            If label_list == False, it will not showed.
        order: Allow to modify the order in what columns are showed,
            allowing to supress column too.
        data_type_list: Allow to modify the data_type that render
            system asign to a column.
            If it is not provided, the program will try to find out what
                data type have each column.
        priority_list: Allow to modify the priority that is assigned to
            each column, if it is not provided,
            the program will asign priorities based on data_type_list.
        If the space to show columns is not sufficient, the program will
            start to supress columns
        (starting with lowest priority column).
        width: Allow to specify width to columns.
            If it is False, same width will be asigned to each column.
            If it is not provided, the program will asign width
                automatically based in priority_list.
        row_separator: It allow to specify a separator between rows.
        page: Allow to specify a page of the record
            (useful if your screen dont allow to view all the render).
        """
        #######################################
        # --- INTEGRITY CHECK IN THE DATA --- #
        #######################################
        # --- The existence of data is checked. --- #
        if data is None:
            return '--- Table > Render: Data to print was not provided. ---'

        # --- Handling for empty data. --- #
        if data == []:
            return '--- EMPTY ---'

        """
        If specified in configuration,
        the data integrity is checked.
        """
        if self.check_data:
            if self.check_data_integrity(data):
                return '--- Table > Render > check_data_integrity: '\
                       'Corrupt or invalid data. ---'

        """
        If specified in configuration,
        the data size is checked.
        """
        if self.check_table_size:
            if self.check_correct_table_size(data):
                return '--- Table > Render: The data '\
                       'dimensions are incongruent. --- '

        ###########################
        # --- PRE-RENDER AREA --- #
        ###########################
        # --- The screen measures are obtained. --- #
        screen_x, screen_y = widgets.measure_screen(
            screen_x=screen_x,
            screen_y=screen_y
            )

        # --- The correction value is applied to screen_x. --- #
        screen_x += self.corrector

        # --- The separator is checked. --- #
        separator = self.check_separator(
            separator=separator,
            screen_x=screen_x
            )

        # --- The row_separator is checked. --- #
        row_separator = self.check_row_separator(
            row_separator=row_separator,
            screen_x=screen_x
            )

        # --- Page value is checked. --- #
        page, page_height = self.check_page_value(
            page=page,
            label_list=label_list,
            screen_y=screen_y
            )

        # --- The validity of provided order is checked. --- #
        order = self.check_order(
            data=data,
            order=order
            )

        # --- The data is rearranged. --- #
        rearranged_data = self.rearrange_data(
            data=data,
            order=order
            )

        # --- Checks the maximum length required to
        # show each field of rearranged_data. --- #
        maximum = self.check_maximums(
            rearranged_data=rearranged_data
            )

        # --- The integrity of data_type_list is checked. --- #
        data_type_list = self.check_data_type_list_integrity(
            label_list=label_list,
            priority_list=priority_list,
            data=data,
            data_type_list=data_type_list
            )

        # --- data_type_list is rearranged. --- #
        rearranged_data_type_list = self.rearrange_data_type_list(
            data_type_list=data_type_list,
            order=order
            )

        # --- The integrity of priority_list is checked, if not exist or if it
        # have defects, the program will try to rebuild it. --- #
        priority_list = self.check_priority_list(
            rearranged_data_type_list=rearranged_data_type_list,
            priority_list=priority_list
            )

        # --- Asign the width to show each column,
        # if it is not provided, the system will try to rebuild it. --- #
        width, order = self.assign_column_width(
            width=width,
            ordered_priority_list=priority_list,
            maximum=maximum,
            screen_x=screen_x,
            len_separator=widgets.printed_length(separator),
            len_order=len(order)
            )

        # --- For twice data_type_list is rearranged. --- #
        rearranged_data_type_list = self.rearrange_data_type_list(
            data_type_list=data_type_list,
            order=order
            )

        # --- For twice data is rearranged. --- #
        rearranged_data = self.rearrange_data(
            data=data,
            order=order
            )
        # --- Label list is checked. --- #
        label_list = self.check_label_list(
            label_list=label_list,
            data_type_list=data_type_list,
            width=width,
            order=order,
            separator=separator
            )

        #######################
        # --- RENDER AREA --- #
        #######################
        # --- The fields that contains the data are generated. --- #
        frame_lines = self.generate_table_frames(
            rearranged_data=rearranged_data,
            width=width,
            maximum=maximum,
            screen_y=screen_y
            )

        # --- Generates the table area that contains the data. --- #
        pre_table = self.generate_pre_table(
            frame_lines=frame_lines,
            separator=separator,
            row_separator=row_separator
            )

        ############################
        # --- POST-RENDER AREA --- #
        ############################
        # --- It do the post_render, joining the pre_table
        # with the other data (labels). --- #
        return self.post_render(
            pre_table=pre_table,
            label_list=label_list,
            len_separator=widgets.printed_length(separator),
            page=page,
            page_height=page_height
            )

    def demo(self):
        """Demonstration function."""
        input('--- Press ENTER to see the dataset as is ---\n')
        print(dataset)
        input(
            '\n--- Now press ENTER to see the dataset '
            'renderized by Outfancy ---\n'
            )
        print(self.render(dataset))

    def check_correct_table_size(self, data=None):
        """This function check the table size."""
        # Is checked if data was provided.
        if data is None:
            return 'Table > Render > check_correct_table_size: '\
                   'Data have not provided.'

        # Is checked if the data have more rows than allowed.
        c1 = len(data) > self.maximum_number_of_rows
        c2 = self.maximum_number_of_rows > -1
        return bool(c1 and c2)

    def check_data_integrity(self, data=None):
        """This function check the data integrity."""
        # Is checked if data is provided.
        if not data:
            return 'Table > Render > check_data_integrity: '\
                   'Data was not provided.'

        error = False
        # Is checked if the type of data is a list.
        if not isinstance(data, list):
            error = True
        else:
            # Check if the list have elements, if not, error = True.
            if len(data) > 0:
                # It checks that the elements type of the list are tuples.
                for the_tuple in data:
                    if not isinstance(the_tuple, tuple):
                        error = True
                    if len(the_tuple) > 0:
                        # Is checked that the elements of tuples
                        # are not list or bool.
                        for element in the_tuple:
                            if isinstance(element, (list, bool)):
                                error = True

            if not error:
                # If not errors were detected yet, it check if the
                # tuple number of elements are all the same.
                length_of_first_tuple = len(data[0])
                for the_tuple in data:
                    if len(the_tuple) != length_of_first_tuple:
                        error = True
            else:
                error = True

        if error:
            logging.error(
                '--- Table > Render > check_data_integrity: '
                'Corrupt or invalid data ---'
                )
        return error

    def check_separator(self, separator=None, screen_x=80):
        """
        This function checks if the separator is valid
        and tryto correct it if it is not.
        """
        # --- It checks if separator is a string,
        # if not, return the default separator. --- #
        if not isinstance(separator, str):
            return ' '
        # It checks if the length of the separator is greater than
        # screen width, if it is the case, the separator is shortened.
        elif widgets.printed_length(separator) > screen_x:
            logging.error(
                'Table > Render > check_separator: '
                'The provided separator is invalid.'
                )
            return ' '
        else:
            return separator

    def check_row_separator(self, row_separator=None, screen_x=80):
        """
        This function check if the row_separator is valid
        and try to correct it if it is not.
        """
        # --- It checks if separator is a string, if not,
        # the row_separator is returned as None --- #
        if not isinstance(row_separator, str):
            return None

        # It checks if the length of the row_separator is less
        # than screen width, if it is, the row_separator is corrected.
        if widgets.printed_length(row_separator) < screen_x:
            row_separator_w_c = widgets.remove_colors(row_separator)

            row_separator_screen_amt = int(
                screen_x / widgets.printed_length(row_separator)
                )

            row_separator = f'{row_separator}'\
                            f'{row_separator_w_c * row_separator_screen_amt}'

        # It checks if the length of the row_separator is greater
        # than screen width, if it is, the separator is shortened.
        if widgets.printed_length(row_separator) > screen_x:
            row_separator = f'{row_separator[:screen_x]}\x1b[0;39m'

        return row_separator

    def check_page_value(self, page, label_list, screen_y):
        """This function check the page value and set the page heigth."""
        if page is None:
            page_height = None
            return page, page_height

        if label_list is False:
            value_to_rest = 0
        else:
            value_to_rest = 1

        page_height = screen_y - value_to_rest

        return page, page_height

    def check_order(self, data=None, order=None):
        """
        This function checks if the order is valid,
        if is not, it will try to rebuild it.
        """
        if data is None:
            logging.error(
                'Table > Render > check_order: Data was not provided.'
                )
            return []

        # --- The validity of provided order is checked
        # based on his properties. --- #
        if not isinstance(order, list):
            logging.error(
                'Table > Render > check_order: '
                'The order is invalid or was not provided.'
                )
            if len(data) > 0:
                order = [x for x in range(len(data[0]))]
                return order
            else:
                return []

        # --- Is analized if the order elements are
        # valid in reference of the data. --- #
        # List of elements to remove.
        to_remove = []
        if len(data) > 0:
            # For each element in len(order).
            for x in range(len(order)):
                # If element is numeric.
                if str(order[x]).isdigit():
                    # If the number order[x] contain is greater than columns
                    # number of data or less than 0 this value is removed.
                    if order[x] >= len(data[0]) or order[x] < -1:
                        to_remove.append(order[x])
                # If element is not numeric, it is removed.
                else:
                    to_remove.append(order[x])
        else:
            return []

        for x in to_remove:
            order.pop(x)

        return order

    def rearrange_data(self, data=None, order=None):
        """
        This function rearrange columns based
        in the data and the order provided.
        """
        # Is checked if data was provided.
        if data is None:
            return 'Table > Render > rearrange_data: Data was not provided.'

        # Is checked if the order input to rearrange_data is valid.
        if not isinstance(order, list):
            # If it is not valid, the data is returned without rearrange.
            return data

        rearranged_data = []
        for the_tuple in data:
            new_tuple = []
            # The rearranged tuple is generated.
            for element in order:
                if widgets.index_is_in_list(the_list=the_tuple, index=element):
                    new_tuple.append(the_tuple[element])
                else:
                    logging.error(
                        'Table > Render > rearrange_data: '
                        'Error when trying to rearrange data.'
                        )
                    return data
            # The generated tuple is added to rearranged_data.
            rearranged_data.append(new_tuple)

        # The rearranged data is returned.
        return rearranged_data

    def check_maximums(self, rearranged_data=None):
        """Check the maximum length of a field in each column,
        # and asing this length to maximum[x]."""
        # Is checked if data is provided.
        if rearranged_data is None:
            return 'Table > Render > check_maximums: '\
                   'Rearranged data was not provided.'

        if len(rearranged_data) > 0:
            # Fill of zeros the maximum values of each element.
            maximum = [0 for column in rearranged_data[0]]
            # Measure the table elements and assing the maximum
            # of each column in each element of maximums list.
            for the_tuple in range(len(rearranged_data)):
                for element in range(len(rearranged_data[0])):
                    field_printed_length = widgets.printed_length(
                        str(rearranged_data[the_tuple][element])
                        )
                    if field_printed_length > maximum[element]:
                        maximum[element] = field_printed_length
            return maximum
        else:
            logging.error(
                'Table > Render > check_maximums: '
                'Error when trying to check maximums.'
                )

    def check_data_type_list_integrity(
        self,
        label_list=False,
        priority_list=None,
        data=None,
        data_type_list=None
            ):
        """This function check the integrity of data_type_list."""
        # If label_list and priority_list are False, data_type_list
        # is not checked because is irrelevant in this use-case.
        if label_list is False and priority_list is False:
            return False

        # Is checked if data was provided.
        if data is None:
            return 'Table > Render > check_data_type_list_integrity: '\
                   'Data was not provided.'

        # An error is emitted if data_type_list is not provided.
        if data_type_list is None:
            logging.error(
                'Table > Render > check_data_type_list_integrity: '
                'data_type_list was not provided.'
                )

        # --- List of columns numbers whose
        # type should try to be detected. --- #
        to_rebuild = []
        # Is checked if tuples exist in data provided.
        if len(data) > 0:
            # If data_type_list is not valid,
            # a new list is prepared to rebuild it.
            if not isinstance(data_type_list, list):
                data_type_list = []
                for x in range(len(data[0])):
                    data_type_list.append(None)
                    to_rebuild.append(x)

            # If data_type_list have more elements that the number
            # of columns of the data the list is shortened.
            if len(data_type_list) > len(data[0]):
                data_type_list = data_type_list[:len(data[0])]
                logging.warning(
                    'Table > Render > check_data_type_list_integrity: '
                    'data_type_list was shortened.'
                    )
            # If it is shorter, missing elements of
            # data_type_list are filled with None.
            elif len(data_type_list) < len(data[0]):
                logging.warning(
                    'Table > Render > check_data_type_list_integrity: '
                    'data_type_list is too short.'
                    )
                for x in range(len(data_type_list), len(data[0])):
                    data_type_list.append(None)

            counter = 0
            # --- Is checked if the elements of data_type_list
            # belong to supported types --- #
            for element in data_type_list:
                if element not in [
                    'id',
                    'name',
                    'date',
                    'time',
                    'value',
                    'desc',
                    None
                        ]:
                    # If not belong, the element will be rebuilded.
                    to_rebuild.append(counter)
                counter += 1

            # --- Is checked and established the
            # quantity of tuples to analyze --- #
            if len(data) > self.analyze_threshold:
                analyze = self.analyze_threshold
            else:
                analyze = len(data)

            ###########################
            # --- Rebuild section --- #
            ###########################
            # --- Is checked if exist data to rebuild --- #
            if len(to_rebuild) > 0:
                # --- The missing or invalid elements of
                # the list are rebuilded --- #
                for x in to_rebuild:
                    # --- Each element of column is analyzed,
                    # trying to determine what type it belongs to. --- #
                    # list_of_types store the detected types.
                    list_of_types = []
                    # --- For each element in the
                    # range of tuple to analyze. --- #
                    for the_tuple in range(analyze):
                        # data[the_tuple][x], is an element of column.
                        field = str(data[the_tuple][x])
                        # --- Check if the element is numeric --- #
                        if field.isdigit():
                            # Try to identify if the element
                            # is a value or an Id.
                            # If length of data is less than two is
                            # impossible to know if a value is an Id or not.
                            if len(data) > 1:
                                # It checks if elements are a
                                # continious sequence, i.e 1, 2, 3, 4.
                                if widgets.index_is_in_list(
                                    the_list=data, index=the_tuple + 1
                                        ):
                                    next_field = str(data[the_tuple + 1][x])
                                    if next_field.isdigit():
                                        if int(next_field) - int(field) == 1:
                                            the_type = 'id'
                                        else:
                                            the_type = 'value'
                                    else:
                                        the_type = 'desc'
                                else:
                                    the_type = 'value'
                                if the_tuple != 0:
                                    if widgets.index_is_in_list(
                                        the_list=data, index=the_tuple - 1
                                            ):
                                        previous_field = str(
                                            data[the_tuple - 1][x]
                                            )
                                        if previous_field.isdigit():
                                            if int(
                                                field
                                                ) - int(
                                                previous_field
                                                    ) == 1:
                                                the_type = 'id'
                                            else:
                                                the_type = 'value'
                                        else:
                                            the_type = 'desc'
                            else:
                                the_type = 'value'
                        # --- Check if the element correspond to an hour. --- #
                        elif widgets.is_complete_hour(field):
                            the_type = 'time'
                        # --- Check if the element correspond to a date. --- #
                        elif widgets.is_date(field):
                            the_type = 'date'
                        # --- If is not numeric, time, or date,
                        # it is assumed that is a text --- #
                        else:
                            if widgets.printed_length(
                                field
                                    ) > self.chk_dlti_num_letters_in_field:
                                num_letters = 0
                                # The number of letters in the
                                # element is counted.
                                for letter in field:
                                    if letter in ascii_letters:
                                        num_letters += 1
                                # If the field have 90% or more of letters
                                # its assumed that it is a name.
                                c_if = self.chk_dlti_pecentage_letters_in_field
                                if (
                                    num_letters * 100 / widgets.printed_length(
                                        field
                                        )
                                        ) > c_if:
                                    the_type = 'name'
                                else:
                                    the_type = 'desc'
                            else:
                                the_type = 'name'

                        # The type is added to the generated list_of_types.
                        list_of_types.append(the_type)

                    # --- The obtained data is analyzed
                    # (belonging to a column) --- #
                    date_type = 0
                    time_type = 0
                    id_type = 0
                    value_type = 0
                    name_type = 0
                    desc_type = 0
                    for the_type in list_of_types:
                        if the_type == 'date':
                            date_type += 1
                        elif the_type == 'time':
                            time_type += 1
                        elif the_type == 'id':
                            id_type += 1
                        elif the_type == 'value':
                            value_type += 1
                        elif the_type == 'name':
                            name_type += 1
                        elif the_type == 'desc':
                            desc_type += 1
                    # --- The analysis data is processed and
                    # integrated to priority list --- #
                    # The percentages of each type over analyze are obtained.
                    date_type *= 100 / analyze
                    time_type *= 100 / analyze
                    id_type *= 100 / analyze
                    value_type *= 100 / analyze
                    name_type *= 100 / analyze
                    desc_type *= 100 / analyze
                    # --- It follows that the resulting type is based
                    # in the correspondency of results with the thresholding.
                    if date_type >= self.chk_dtli_date:
                        the_type = 'date'
                    elif time_type >= self.chk_dtli_time:
                        the_type = 'time'
                    elif id_type >= self.chk_dtli_id:
                        the_type = 'id'
                    elif value_type >= self.chk_dlti_value:
                        the_type = 'value'
                    elif name_type >= self.chk_dlti_name:
                        the_type = 'name'
                    elif desc_type >= self.chk_dlti_desc:
                        the_type = 'desc'
                    else:
                        the_type = 'desc'

                    # The type found is assigned to corresponding
                    # element in data_type_list.
                    data_type_list[x] = the_type

            if len(to_rebuild) > 0:
                logging.warning(
                    'Table > Render > check_data_type_list_integrity: '
                    'data_type_list was rebuilded of modified.'
                    )

            # The data_type_list is returned.
            return data_type_list

    def rearrange_data_type_list(self, data_type_list=None, order=None):
        """This function rearrange data_type_list based on provided order."""
        # Is checked if data_type_list was provided.
        if data_type_list is None:
            raise Exception(
                'Table > Render > rearrange_data_type_list: '
                'data_type_list was not provided.'
                )

        # If order is not provided, or if it is not list,
        # data_type_list is returned.
        if not isinstance(order, list):
            logging.error(
                'Table > Render > rearrange_data_type_list: '
                'The order was not provided or is not valid.'
                )
            return data_type_list
        else:
            rearranged_data_type_list = []
            # The rearranged tuple is generated.
            for element in order:
                if widgets.index_is_in_list(
                    the_list=data_type_list,
                    index=element
                        ):
                    rearranged_data_type_list.append(data_type_list[element])
                else:
                    logging.error(
                        'Table > Render > rearrange_data_type_list: '
                        'Error when trying to rearrange data_type_list.'
                        )
                    return data_type_list
            # If rearrange process finish without errors,
            # the rearranged data_type_list is returned.
            return rearranged_data_type_list

    def check_priority_list(
        self,
        rearranged_data_type_list=None,
        priority_list=None,
            ):
        """
        This function checks the integrity of the priority_list,
        in case or be defficient (or ausent), try to rebuild it.
        """
        # If label_list is False, it will be returned it,
        # because this value is valid in other parts of the program.
        if priority_list is False:
            return priority_list

        if rearranged_data_type_list is None:
            raise Exception(
                'Table > Render > check_priority_list: '
                'rearranged_data_type_list was not provided.'
                )

        # Length of rearranged_data_type_list
        len_rearranged_data_type_list = len(rearranged_data_type_list)

        ########################
        #   INTEGRITY CHECKS   #
        ########################
        # Bool variable to check if reconstruction is needed or not.
        rebuild = False

        # If priority_list is None.
        if not isinstance(priority_list, list):
            rebuild = True
            logging.error(
                'Table > Render > check_priority_list: '
                'priority_list was not provided or is not valid.'
                )
        else:
            # Length of priority_list.
            len_priority_list = len(priority_list)

            # If priority_list is not None.
            if priority_list is not None:
                # If an element of priority_list
                # is not numeric. rebuild is True.
                for x in priority_list:
                    if not isinstance(x, int):
                        rebuild = True

            # If len_priority_list is greater than
            # rearranged_data_type_list, rebuild = True.
            if len_priority_list > len_rearranged_data_type_list:
                logging.warning(
                    'Table > Render > check_priority_list: '
                    'priority_list is too long.'
                    )
                rebuild = True

            # If len_priority_list is shorter than
            # rearranged_data_type_list, rebuild = True.
            if len_priority_list < len_rearranged_data_type_list:
                logging.warning(
                    'Table > Render > check_priority_list: '
                    'priority_list is too short.'
                    )
                rebuild = True

            # The integrity of elements is checked.
            for x in priority_list:
                if x >= len_rearranged_data_type_list or x < 0:
                    rebuild = True
                if rebuild:
                    logging.warning(
                        'Table > Render > check_priority_list: '
                        'priority_list is not valid.'
                        )

        # If rebuild is needed.
        if rebuild:
            # An empty priority_list is declared.
            priority_list = []

            # It tries to identify Id and Value elements,
            # maximum priority is assigned to it.
            for element in range(len_rearranged_data_type_list):
                if rearranged_data_type_list[element] in ['id', 'value']:
                    priority_list.append(element)

            # It tries to identify name elements,
            # assigning the corresponding priority.
            for element in range(len_rearranged_data_type_list):
                if rearranged_data_type_list[element] == 'name':
                    priority_list.append(element)

            # It tries to identify date elements,
            # assigning the corresponding priority.
            for element in range(len_rearranged_data_type_list):
                if rearranged_data_type_list[element] == 'date':
                    priority_list.append(element)

            # It tries to identify time elements,
            # assigning the corresponding priority.
            for element in range(len_rearranged_data_type_list):
                if rearranged_data_type_list[element] == 'time':
                    priority_list.append(element)

            # It tries to identify desc elements,
            # assigning the corresponding priority.
            for element in range(len_rearranged_data_type_list):
                if rearranged_data_type_list[element] == 'desc':
                    priority_list.append(element)

            # If exists elements without identify in rearranged_data_type_list,
            #   the missing elements of the lists
            #   are filled with minimal priorities.
            if len(priority_list) < len_rearranged_data_type_list:
                logging.warning(
                    'Table > Render > check_priority_list: '
                    'rearranged_data_type_list have uncategorizable elements.'
                    )
                for element in range(
                    len(priority_list), len_rearranged_data_type_list
                        ):
                    priority_list.append(element)
        return priority_list

    def assign_column_width(
        self,
        width=None,
        ordered_priority_list=False,
        maximum=None,
        screen_x=None,
        len_separator=None,
        len_order=None
            ):
        """Asign the width to each column."""
        if width:
            order = [x for x in range(len(width))]
            return width, order

        # If len_separator is not provided or is less than 0,
        # it will be asigned to 1 and an error will be emitted.
        if not isinstance(len_separator, int) or len_separator < 0:
            len_separator = 1
            logging.error(
                'Table > Render > assign_column_width: '
                'len_separator was not provided or it is invalid.'
                )

        # If len_order and ordered_priority_list was not provided.
        c1 = isinstance(ordered_priority_list, list)
        if len_order is None and maximum is None and not c1:
            raise Exception(
                'Table > Render > assign_column_width: ordered_priority_list '
                'and len_order and maximum was not provided.'
                )

        # If len_order is not provided or is less than 0,
        # it will be asigned to 1 and an error will be emitted.
        if not isinstance(len_order, int) or len_order < 0:
            logging.error(
                'Table > Render > assign_column_width: '
                'len_order was not provided or it is invalid.'
                )

        # The system check len_order, and if it is invalid,
        # try to rebuild it based on len(ordered_priority_list).
        if len_order is None and isinstance(ordered_priority_list, list):
            len_order = len(ordered_priority_list)

        # The system check len_order, and if it is invalid,
        # try to rebuild it based on len(maximum).
        if len_order is None and isinstance(maximum, list):
            len_order = len(maximum)

        def get_medium_width(remaining_space, len_order):
            """Get the medium width based on remaining_space."""
            if len_order == 0:
                return 0
            else:
                return int(remaining_space / len_order)

        def get_screen_x_axis_space():
            """
            Calculate the space on screen removing
            the length of the separators to screen_x.
            """
            return screen_x - len_separator * len_order

        # The order that assign_column_width take as basis at hour of
        # communicate the change made in general variables.
        order = [x for x in range(len_order)]

        # If width is provided, is checked, and,
        # in case of being valid, it is returned.
        to_rebuild = False
        total_length_of_elements = 0
        # If the element is a list.
        if isinstance(width, list):
            # Is checked that each element are numeric,
            # and his sum is not greater than remaining_space.
            for element in width:
                if isinstance(element, int):
                    if element > 0:
                        total_length_of_elements += element
                    else:
                        to_rebuild = True
                else:
                    to_rebuild = True
        else:
            to_rebuild = True

        # If the width total is greater than screen space
        # (screen_x_axis_space()), it will be rebuilded.
        if total_length_of_elements > get_screen_x_axis_space():
            to_rebuild = True

        # If the check demonstrats that all is fine,
        # the width list and order list are returned.
        if not to_rebuild:
            return width, order

        # If screen_x is None or less than 1, 80 (a common value (See:
        # IBM Cards, World War II), and an error is emitted).
        if not isinstance(screen_x, int) or screen_x < 1:
            screen_x = 80
            logging.warning(
                'Table > Render > assign_column_width: '
                'screen_x was not provided or it is invalid.'
                )

        # If show_width_threshold is not provided or is less than 1,
        # it is assigned to 5 and an error is emitted.
        c1 = isinstance(self.show_width_threshold, int)
        c2 = self.show_width_threshold < 1
        if not c1 or c2:
            self.show_width_threshold = 5
            logging.warning(
                'Table > Render > assign_column_width: '
                'show_width_threshold was not provided or it is invalid.'
                )

        # If ordered_priority_list == False,
        # it is asigned the same width to same columns based in len(order).
        # If maximum was not provided or it is invalid an
        # error is emitted and maximum is rebuilded.
        c1 = isinstance(maximum, list)
        if not c1 or ordered_priority_list is False or width is False:
            logging.warning(
                'Table > Render > assign_column_width: '
                'Maximum was not provided or it is invalid.'
                )
            maximum = []

            checking = True
            while checking:
                if len_order > 0:
                    medium_width = get_medium_width(
                        remaining_space=get_screen_x_axis_space(),
                        len_order=len_order
                        )
                    # If medium_width is less or equal to 0.
                    if medium_width <= 0:
                        # The element of less priority is removed.
                        # And the list is compressed to maintain
                        # the congruency of data.
                        ordered_priority_list = widgets.compress_list(
                            ordered_priority_list[:len_order - 1]
                            )
                        len_order -= 1
                    else:
                        checking = False
                else:
                    medium_width = 0
                    checking = False

            # The maximum for each column are equals to the
            # medium_width obtained in screen width function.
            for x in range(len_order):
                maximum.append(medium_width)

        # Priority_list is checked.
        c1 = isinstance(ordered_priority_list, bool)
        if c1 or ordered_priority_list is None:
            ordered_priority_list = [x for x in range(len_order)]

        not_finished = True
        while not_finished:
            # A list full of zeroes which will contain width is generated.
            width = [0 for x in range(len_order)]
            # List to record maximum less than show_width_threshold.
            maxima_less_than_show_width_threshold = []

            # remaining_space is initialized with a value that equals to
            # screen_x_axis_space, when it being used it will be shortened.
            remaining_space = get_screen_x_axis_space()

            # For each element of priority_list.
            # Take account that the space is asigned
            # starting with the major priority.
            for column in range(len_order):
                # The medium_width of available columns is obtained.
                medium_width = get_medium_width(
                    remaining_space=remaining_space,
                    len_order=len_order
                    )

                # If maximum[column] is less than medium_width
                # this value is assigned.
                if maximum[column] < medium_width:
                    width[column] = maximum[column]
                    if maximum[column] < self.show_width_threshold:
                        maxima_less_than_show_width_threshold.append(column)
                # If maximum[column] is greater the width
                # will be equal to medium_width.
                else:
                    width[column] = medium_width

                # remaining_space is recalculated.
                remaining_space -= width[column]
                # A column is removed (from len_order)
                # (because the space of a column is now assigned).
                len_order -= 1

            # The assignement process is marked as finished,
            # but the posterior checking can assign True to not_finished.
            not_finished = False

            len_width = len(width)
            # --- If assigned width exists. ---#
            # The greater than 1 width check is used in case that
            # the screen only have a column, allowing this column
            #    to dissobey medium_width less to maximum[column],
            # reducing the column width anyway.
            if len_width > 1:
                # Is checked if exists elements below show_width_threshold,
                # if it is the case, and the element is not in
                #    maxima_less_than_show_width_thresold, not_finished = True.
                for column in range(len_width):
                    if width[column] < self.show_width_threshold:
                        if column not in maxima_less_than_show_width_threshold:
                            not_finished = True

            if not_finished:
                # The index to remove is determinated
                # (indicated by the last element of ordered_priority_list).
                index_to_remove = ordered_priority_list[len_order - 1]
                # Index_to_remove is removed to order.
                order.pop(index_to_remove)
                # Index_to_remove is removed from maximum list.
                maximum.pop(index_to_remove)
                # The last element is removed from ordered_priority_list
                # (the lower priority), later, the list.
                #    is compressed (to ensure the integrity
                #    of the date registered in that list).
                ordered_priority_list = widgets.compress_list(
                    ordered_priority_list[:len_order - 1]
                    )
                # len_order is recalculated.
                len_order = len(ordered_priority_list)
        return width, order

    def generate_table_frames(
        self,
        rearranged_data=None,
        width=None,
        maximum=None,
        screen_y=None
            ):
        """Generate the table frames, where the text is contained."""
        # --- If data is not provided, an empty list is returned --- #
        if rearranged_data is None:
            logging.error(
                'Table > Render > generate_table_frames: '
                'rearranged_data was not provided.'
                )
            return []

        # --- If column width list was not provided,
        # an empty list is returned. --- #
        if width is None:
            logging.error(
                'Table > Render > generate_table_frames: '
                'Column width list was not provided.'
                )
            return []

        # --- If maximums list is not provided, an empty list is returned --- #
        if maximum is None:
            logging.error(
                'Table > Render > generate_table_frames: '
                'maximums list was not provided.'
                )
            return []

        # Frame_lines store the lines that are generated.
        frame_lines = []
        for the_tuple in range(len(rearranged_data)):
            # Each field of tuple are analyzed.
            frame_to_insert = []
            for column in range(len(width)):
                # --- A frame is generated --- #
                after = width[column]
                frame = []
                field_to_process = str(rearranged_data[the_tuple][column])
                # --- While frame´s length is greater
                # than column width, it is cutted. --- #
                if width[column] > 0:
                    # If width[column] is equal or less than 0,
                    # it will be cutted infinitely.
                    while widgets.printed_length(
                        field_to_process
                            ) > width[column]:
                        frame.append(field_to_process[:after])
                        field_to_process = field_to_process[after:]
                # --- If field_to_process and width[column] are equals,
                # the frame is appended without any process. --- #
                if widgets.printed_length(field_to_process) == width[column]:
                    frame.append(field_to_process)
                # --- If the content of the frame to cut is lower than column
                # width the required space is filled of whitespaces. --- #
                if widgets.printed_length(field_to_process) < width[column]:
                    after_space = ' ' * (
                        width[column] - widgets.printed_length(
                            field_to_process
                            )
                        )
                    frame.append(f'{field_to_process}{after_space}')
                # --- The generated frame is cutted in function of
                # max_heigth_of_a_tuple (maximum heigth). --- #
                c1 = len(frame) > self.max_heigth_of_a_tuple
                c2 = self.max_heigth_of_a_tuple >= 0
                if c1 and c2:
                    frame = frame[:self.max_heigth_of_a_tuple]

                # --- Each frame is inserted in the field
                # that is being generated. --- #
                frame_to_insert.append(frame)

            # --- Maximum space (y axis) for each frame is checked --- #
            maximum = 0
            for frame in frame_to_insert:
                if len(frame) > maximum:
                    maximum = len(frame)
            # --- The missing lines in each field are filled
            # with white lines to get equal heigth fields. --- #
            for column in range(len(frame_to_insert)):
                # If the length of frame is lower than maximum[frame]
                while len(frame_to_insert[column]) < maximum:
                    frame_to_insert[column].append(' ' * width[column])

            # --- Each field is appended to frame_lines --- #
            frame_lines.append(frame_to_insert)

        # --- frame_lines list is returned --- #
        return frame_lines

    def generate_pre_table(
        self,
        frame_lines=None,
        separator=None,
        row_separator=None
            ):
        """
        This function join the fields and separator,
        creating the data area of the table.
        """
        # Check if frame_lines is provided, if it is not, return an error.
        if frame_lines is None:
            return 'Table > Render > generate_pre_table: '\
                   'frame_lines was not provided.'

        # If separator is not provided is assigned by default to " ".
        if separator is None:
            logging.warning(
                'Table > Render > generate_pre_table: '
                'searator was not provided.'
                )
            separator = ' '

        # pre_table start as an empty string,
        # it will be filled with the frame_lines.
        pre_table = ''
        # --- For each row of frame_lines. --- #
        for row in range(len(frame_lines)):
            the_tuple = frame_lines[row]
            if len(the_tuple) > 0:
                # For each line in the range of number that
                # equals to heigth of the row in the table.
                for line in range(len(the_tuple[0])):
                    # --- A line of each field will be added to pre_table,
                    # and will be integrated with the separator. --- #
                    for field in the_tuple:
                        pre_table += f'{separator}{field[line]}'

                    pre_table += '\n'

                # --- If row_separator is provided --- #
                if row_separator:
                    # The row_separator is added to pre_table.
                    pre_table += f'{row_separator}\n'

        # --- If row_separator is provided --- #
        if row_separator:
            # If in config separator before table is activated.
            if self.row_separator_before_table:
                # The row_separator is added before the table.
                pre_table = f'{row_separator}\n{pre_table}'

        # If pre_table ends with \n (ENTER), this last ENTER is removed.
        if len(pre_table) > 0:
            if pre_table[len(pre_table) - 1] == '\n':
                pre_table = pre_table[:len(pre_table) - 1]

        # pre_table is returned.
        return pre_table

    def check_label_list(
        self,
        label_list=None,
        data_type_list=None,
        width=None,
        order=None,
        separator=None
            ):
        """
        This function check the label_list, if it do not exist or it is
        invalid, it will try to rebuild it.
        """
        # If label_list is False, this value is returned,
        # because it have validity in other parts of the program.
        if label_list is False:
            return label_list

        # If data_type_list is None, an empty string will be returned.
        if data_type_list is None:
            return ''

        # --- If label_list is invalid, it will be rebuilded --- #
        # List of elements that have to be rebuilded.
        to_rebuild = []
        if not isinstance(label_list, list):
            logging.warning(
                'Table > Render > check_label_list: '
                'label_list was not provided or it is invalid.'
                )
            # If the type of label_list is not a list, a new list
            # is generated, and it is filled by None.
            label_list = [None for x in range(len(data_type_list))]

        # Check the type of the data contained in label_list, if some data
        # is not an string, its assigned to None, and it index is added to
        # to_rebuild.
        for x in range(len(label_list)):
            if not isinstance(label_list[x], str) or label_list[x] is None:
                to_rebuild.append(x)
                label_list[x] = None

        # If separator is not provided, it will be restored to ' '.
        if separator is None:
            logging.warning(
                'Table > Render > check_label_list: '
                'The separator was not provided.'
                )
            separator = ' '

        # If label_list have more elements than date_type_lits,
        # label_list is shortened.
        if len(label_list) > len(data_type_list):
            label_list = label_list[:len(data_type_list)]
            logging.warning(
                'Table > Render > check_label_list: label_list was shortened.'
                )
        # Else, the missing elements are filled by None.
        elif len(label_list) < len(data_type_list):
            logging.warning(
                'Table > Render > check_label_list: label_list is too short.'
                )
            for x in range(len(label_list), len(data_type_list)):
                label_list.append(None)
                to_rebuild.append(x)

        # For each element of label_list that need to be rebuild.
        for x in to_rebuild:
            # It try to rebuild each element.
            translate_data_type_to_label = {
                'id': 'Id',
                'name': 'Name',
                'date': 'Date',
                'time': 'Hour',
                'value': 'Value',
                'desc': 'Description'
                }
            if data_type_list[x] in translate_data_type_to_label.keys():
                # The label obtained is assigned to label_list.
                label_list[x] = translate_data_type_to_label[data_type_list[x]]
            else:
                label_list[x] = f'Col.{x}'

        if len(to_rebuild) > 0:
            logging.warning(
                'Table > Render > check_label_list: label_list was rebuilt.'
                )

        # Check if order is provided, if it is not, an error is emmited,
        # else, the labels are rearranged.
        if not isinstance(order, list):
            logging.warning(
                'Table > Render > check_label_list: '
                'Order was not provided or it is invalid.'
                )
            ordered_label_list = label_list
        else:
            ordered_label_list = []
            for element in order:
                if widgets.index_is_in_list(
                    the_list=label_list,
                    index=element
                        ):
                    ordered_label_list.append(label_list[element])
                else:
                    logging.warning(
                        'Table > Render > check_label_list: '
                        'Error when trying to rearrange the labels.'
                        )

        # If width is not provided, an error is emitted and label_list
        # (integrated with separator) is returned.
        if width is None:
            logging.error(
                'Table > Render > check_label_list: '
                'Width list was not provided.'
                )

            joined_label_list = separator.join(ordered_label_list)
            return f'{separator}{joined_label_list}'

        # For each element in length of width list.
        for x in range(len(width)):
            # If length of label is greater than column width,
            # the label is shortened.
            if widgets.printed_length(ordered_label_list[x]) > width[x]:
                ordered_label_list[x] = ordered_label_list[x][:width[x]]
            # Else, the missing space is filled with whitespaces.
            elif widgets.printed_length(ordered_label_list[x]) < width[x]:
                label_length = widgets.printed_length(ordered_label_list[x])
                after_space_length = ' ' * (width[x] - label_length)
                ordered_label_list[x] = f'{ordered_label_list[x]}'\
                    f'{after_space_length}'

        # Ordered label list (integrated with separator) is returned.
        joined_label_list = separator.join(ordered_label_list)
        return f'{separator}{joined_label_list}'

    def post_render(
        self,
        pre_table=None,
        label_list=None,
        len_separator=None,
        page=None,
        page_height=None
            ):
        """
        This function join the table, the labels and the errors
        (depending of the configuration).
        """
        # If pre_table is not provided an error is emitted.
        if pre_table is None:
            logging.error(
                'Table > Render > post_render: pre_table was not provided, '
                'this can occur if the data is not valid.'
                )
            pre_table = ''

        # If the length of separator is not provided, an error is emitted
        # and the variable is assigned to 1.
        if len_separator is None:
            logging.warning(
                'Table > Render > post_render: '
                'len_separator was not provided.'
                )
            len_separator = 1

        # If label_list is not provided, it is asigned to False,
        # and it not will showed.
        if label_list is None:
            logging.warning(
                'Table > Render > post_render: '
                'label_list was not provided.'
                )
            label_list = False

        # If page is provided.
        if page:
            # Values to cut the table are calculated.
            first_row = page * page_height
            last_row = first_row + page_height

            if first_row < 0 or first_row > len(pre_table):
                first_row = len(pre_table)

            if last_row < 0 or last_row > len(pre_table):
                last_row = len(pre_table)

            # pre_table is cutted to show the desired page.
            pre_table = pre_table.split('\n')
            pre_table = pre_table[first_row: last_row]
            pre_table = ' '.join(pre_table)

        # Variable that store the render.
        post_rendering = ''

        # If label_list is not False, and show_labels is True,
        # label_list are added to post_rendering.
        if label_list is not False and self.show_labels:
            post_rendering += f'\x1b[1;33m{label_list}\x1b[0;99m\n'

        # The pre_table (render of the table data) is added to post_rendering.
        post_rendering += f'{pre_table}\x1b[0;99m'

        # Post_rendering is returned.
        return post_rendering


class Oneline:
    """
    Oneline is a class prepared to do printing line by line.
    - In the same way as Table instances, the usage is self.table.render(data),
    - To use this function is highly recommended that width parameters
        are well asigned.
    - Oneline creates an instance of Table, configurating it on a way that
        enable it to work line by line.
    """
    def __init__(self):
        # The table object is generated. (as instance of Table).
        self.table = Table()
        self.table.set_maximum_number_of_rows(1)
        self.table.set_row_separator_before_table(False)

    def set_check_data(self, x=False):
        """
        If check_data == True the dataset input will be checked. If you
        don't trust the data source, enable the data checking.
        """
        self.table.check_data = x

    def set_check_table_size(self, x=False):
        """
        If check_table_size == True, the measures of the table will be
        checked. If you don't trust the data source, enable the data measuring.
        """
        self.table.check_table_size = x

    def set_corrector(self, x=-2):
        """
        The corrector is a value that will be added to
        screen_x length, is -2 by default.
        """
        self.table.corrector = x

    def set_max_heigth_of_a_tuple(self, x=20):
        """
        The analyze threshold is the number of tuples that will
        be analyzed in check_data_type_list_integrity.
        """
        self.table.max_heigth_of_a_tuple = x

    def set_show_width_threshold(self, x=True):
        """
        This function show the width threshold, below the width
        threshold, a column will not be showed.
        """
        self.table.show_width_threshold = x

    def set_maximum_number_of_rows(self, x=1):
        """
        This function allow to modify the maximum number of rows
        that outfancy can show, by default is infinite (-1).
        """
        self.table.maximum_number_of_rows = x

    def set_row_separator_before_table(self, x=True):
        """
        Row_separator_before_table allow to enable or
        disable the separator before the table.
        """
        self.table.row_separator_before_table = x

    def show_check_data(self):
        """It shows the value of the variable check_data."""
        print(self.table.check_data)

    def show_check_table_size(self):
        """It shows the value of the variable check_table_size."""
        print(self.table.check_table_size)

    def show_corrector(self):
        """It shows the value of the corrector."""
        print(self.table.corrector)

    def show_max_heigth_of_a_tuple(self):
        """It shows the value of the variable max_heigth_of_a_tuple."""
        print(self.table.max_heigth_of_a_tuple)

    def show_show_width_threshold(self):
        """It shows the value of the variable show_width_threshold."""
        print(self.table.show_width_threshold)

    def show_maximum_number_of_rows(self):
        """It shows the value of the variable maximum_number_of_rows."""
        print(self.table.maximum_number_of_rows)

    def show_row_separator_before_table(self):
        """It shows the value of the variable row_separator_before_table."""
        print(self.table.row_separator_before_table)

    def render(
        self,
        data=None,
        width=None,
        separator=None,
        order=None,
        priority_list=None,
        screen_x=None,
        screen_y=None
            ):
        """
        Function that prints a line in each execution, based in
        provided data and configuration.
        The variables this function have are the same as Table.
        """
        # --- If data are provided, it be preparated for rendering. --- #
        if data is None:
            return '--- Oneline > Render: Data to print was not received ---'
        else:
            if isinstance(data, (list, tuple)):
                if len(data) > 0:
                    # If the content of the first element
                    # of the data is not a tuple.
                    if not isinstance(data[0], tuple):
                        # The converted to tuple data are
                        # inserted in an empty list.
                        new_data = [tuple(data)]
                    else:
                        new_data = data
                else:
                    new_data = data

            # The normalized data is renderized.
            # (Remember that Table will apply his own checks).
            return self.table.render(
                data=new_data,
                separator=separator,
                label_list=False,
                order=order,
                priority_list=priority_list,
                width=width,
                screen_x=screen_x,
                screen_y=screen_y
                )

    def demo(self):
        """Demonstration function."""
        from time import sleep
        input('--- Press ENTER to see the dataset as is ---')
        print(dataset)
        input(
            '\n--- Now press ENTER to see the dataset '
            'renderized by Outfancy ---'
            '\n(this function will sleep one second '
            'between rendering each row). ---\n'
            )

        # --- The screen measures are obtained. --- #
        screen_x, screen_y = widgets.measure_screen()

        # --- The validity of provided order is checked. --- #
        order = self.table.check_order(
            data=dataset,
            order=None
            )

        # --- The data is rearranged. --- #
        rearranged_data = self.table.rearrange_data(
            data=dataset,
            order=order
            )

        # --- Checks the maximum length required to
        # show each field of rearranged_data. --- #
        maximum = self.table.check_maximums(
            rearranged_data=rearranged_data
            )

        # --- The integrity of data_type_list is checked. --- #
        data_type_list = self.table.check_data_type_list_integrity(
            label_list=None,
            priority_list=None,
            data=dataset,
            data_type_list=None
            )

        # --- data_type_list is rearranged. --- #
        rearranged_data_type_list = self.table.rearrange_data_type_list(
            data_type_list=data_type_list,
            order=order
            )

        # --- The integrity of priority_list is checked, if not exist or if it
        # have defects, the program will try to rebuild it. --- #
        priority_list = self.table.check_priority_list(
            rearranged_data_type_list=rearranged_data_type_list,
            priority_list=None
            )

        width, order = self.table.assign_column_width(
            width=None,
            ordered_priority_list=priority_list,
            maximum=maximum,
            screen_x=screen_x,
            len_separator=1,
            len_order=len(order)
            )

        for row in dataset:
            print(
                self.render(
                    data=row,
                    width=width,
                    separator=' ',
                    order=order,
                    priority_list=priority_list,
                    screen_x=screen_x,
                    screen_y=screen_y
                    )
                )
            sleep(1)


class LargeTable:
    """
    LargeTable is a class prepared to print large tables
        (thousands of rows or more).

    - It does the render and PRINT the table.

    - LargeTable creates an instance of Table, using it internal
        functions in pre-render tasks.

    - The parameters that can be assigned to render function are the
        same as Table class.
    """
    def __init__(self):
        # The motor object is generated. (as instance of Table)
        self.table = Table()
        self.table.set_maximum_number_of_rows(1)
        self.table.set_row_separator_before_table(False)

        # Numbers of rows to process before the table printing.
        self.rows_to_analyze = 100

    def set_check_data(self, x=False):
        """
        If check_data == True the dataset input will be checked. If you
        don't trust the data source, enable the data checking.
        """
        self.table.check_data = x

    def set_check_table_size(self, x=False):
        """
        If check_table_size == True, the measures of the table will be checked.
        If you don't trust the data source, enable the data measuring.
        """
        self.table.check_table_size = x

    def set_corrector(self, x=-2):
        """
        The corrector is a value that will be added to
        screen_x length, is -2 by default.
        """
        self.table.corrector = x

    def set_max_heigth_of_a_tuple(self, x=20):
        """
        The analyze threshold is the number of tuples that will
        be analyzed in check_data_type_list_integrity.
        """
        self.table.max_heigth_of_a_tuple = x

    def set_show_width_threshold(self, x=True):
        """
        This function show the width threshold, below the width
        threshold, a column will not be showed.
        """
        self.table.show_width_threshold = x

    def set_maximum_number_of_rows(self, x=1):
        """
        This function allow to modify the maximum number of rows
        that outfancy can show, by default is infinite (-1).
        """
        self.table.maximum_number_of_rows = x

    def set_row_separator_before_table(self, x=True):
        """
        Row_separator_before_table allow to enable or disable
        the separator before the table.
        """
        self.table.row_separator_before_table = x

    def show_check_data(self):
        """It shows the value of the variable check_data."""
        print(self.table.check_data)

    def show_check_table_size(self):
        """It shows the value of the variable check_table_size."""
        print(self.table.check_table_size)

    def show_corrector(self):
        """It shows the value of the corrector."""
        print(self.table.corrector)

    def show_max_heigth_of_a_tuple(self):
        """It shows the value of the variable max_heigth_of_a_tuple."""
        print(self.table.max_heigth_of_a_tuple)

    def show_show_width_threshold(self):
        """It shows the value of the variable show_width_threshold."""
        print(self.table.show_width_threshold)

    def show_maximum_number_of_rows(self):
        """It shows the value of the variable maximum_number_of_rows."""
        print(self.table.maximum_number_of_rows)

    def show_row_separator_before_table(self):
        """It shows the value of the variable row_separator_before_table."""
        print(self.table.row_separator_before_table)

    def render(
        self,
        data=None,
        separator=None,
        label_list=None,
        order=None,
        data_type_list=None,
        priority_list=None,
        width=None,
        row_separator=None
            ):

        """Render receive six (6) parameters, and is responsible for the render
        of the data in a table on an organized way.

        Parameters:
        data: It have to be specified in the next format:
            [(1, 'Amelia', 'Lawyer'), (2, 'Camille', 'Chef')].
        separator: It allow to modify the string that separate
            the columns, by default is a white space " ".
        label_list: Allows to modify the label list that
            is showed above renderized table.
            If it is not provided, the program will try to find out
                what label will have each column.
            If label_list == False, it will not showed.
        order: Allow to modify the order in what columns are showed,
            allowing to supress column too.
        data_type_list: Allow to modify the data_type that render
            system assign to a column.
            If it is not provided, the program will try to find out what
                data type have each column.
        priority_list: Allow to modify the priority that is assigned
            to each column, if it is not provided,
            the program will asign priorities based on data_type_list.
        If the space to show columns is not sufficient, the program will
            start to supress columns (starting with lowest priority column).
        width: Allow to specify width to columns.
            If it is False, same width will be asigned to each column.
            If it is not provided, the program will asign width
            automatically based in priority_list.
        row_separator: It allow to specify a separator between rows.
        """
        #######################################
        # --- INTEGRITY CHECK IN THE DATA --- #
        #######################################
        # --- The existence of data is checked --- #
        if data is None:
            return '--- Table > Render: Data to print was not provided. ---'

        # --- Handling for empty data --- #
        if data == []:
            return '--- EMPTY ---'

        # It create a table with data to analyze.
        if len(data) > self.rows_to_analyze:
            data_to_analyze = data[:self.rows_to_analyze]
        else:
            data_to_analyze = data

        # --- If it is specified in configuration,
        #   the data integrity is checked. --- #
        if self.table.check_data:
            if self.table.check_data_integrity(data_to_analyze):
                return '--- Table > Render > check_data_integrity: '\
                       'Corrupt or invalid data. ---'

        # --- If it is specified in configuration,
        # the data size is checked. --- #
        if self.table.check_table_size:
            if self.table.check_correct_table_size(data_to_analyze):
                return '--- Table > Render: '\
                        'The data dimensions are incongruent. ---'

        ###########################
        # --- PRE-RENDER AREA --- #
        ###########################
        # --- The screen measures are obtained --- #
        screen_x, screen_y = widgets.measure_screen()

        # --- The correction value is applied to screen_x --- #
        screen_x += self.table.corrector

        # --- The separator is checked --- #
        separator = self.table.check_separator(
            separator=separator,
            screen_x=screen_x
            )

        # --- The row_separator is checked --- #
        row_separator = self.table.check_row_separator(
            row_separator=row_separator,
            screen_x=screen_x
            )

        # --- The validity of provided order is checked --- #
        order = self.table.check_order(
            data=data_to_analyze,
            order=order
            )

        # --- The data is rearranged --- #
        rearranged_data = self.table.rearrange_data(
            data=data_to_analyze,
            order=order
            )

        # --- Check the maximum length required to
        # show each field of rearranged_data. --- #
        maximum = self.table.check_maximums(
            rearranged_data=rearranged_data
            )

        # --- The integrity of data_type_list is checked --- #
        data_type_list = self.table.check_data_type_list_integrity(
            label_list=label_list,
            priority_list=priority_list,
            data=data_to_analyze,
            data_type_list=data_type_list
            )

        # --- data_type_list is rearranged --- #
        rearranged_data_type_list = self.table.rearrange_data_type_list(
            data_type_list=data_type_list,
            order=order
            )

        # --- The integrity of priority_list is checked, if it does not exist
        # or if it have defects, the program will try to rebuild it. --- #
        priority_list = self.table.check_priority_list(
            rearranged_data_type_list=rearranged_data_type_list,
            priority_list=priority_list
            )

        # --- Assign the width to show each column, if it is not provided,
        # the system will try to rebuild it. --- #
        width, order_2 = self.table.assign_column_width(
            width=width,
            ordered_priority_list=priority_list,
            maximum=maximum,
            screen_x=screen_x,
            len_separator=widgets.printed_length(separator),
            len_order=len(order)
            )

        # --- For twice data_type_list is rearranged --- #
        rearranged_data_type_list = self.table.rearrange_data_type_list(
            data_type_list=data_type_list,
            order=order_2
            )

        # --- Label list is checked. --- #
        label_list = self.table.check_label_list(
            label_list=label_list,
            data_type_list=data_type_list,
            width=width,
            order=order,
            separator=separator
            )

        # --- . --- #
        order = self.get_final_order_list(
            [order, order_2],
            data_to_analyze
            )

        ############################
        # --- POST-RENDER AREA --- #
        ############################

        # --- The label_list is printed --- #
        print(f'\x1b[1;33m{label_list}\x1b[0;99m')

        # --- Each row is processed and printed --- #
        for x_row in range(len(data)):
            #                         #
            # --- PRE-RENDER AREA --- #
            #                         #

            # It generates the row that will be rendered.
            row = []

            # --- The row is rearranged --- #
            rearranged_row = self.rearrange_row(
                row=data[x_row],
                order=order
                )

            #                     #
            # --- RENDER AREA --- #
            #                     #

            # --- The fields that contains the data are generated --- #
            row.append(rearranged_row)
            frame_lines = self.table.generate_table_frames(
                rearranged_data=row,
                width=width,
                maximum=maximum,
                screen_y=screen_y
                )

            # --- Generates the table area that contains rendered_row. --- #
            pre_table = self.table.generate_pre_table(
                frame_lines=frame_lines,
                separator=separator,
                row_separator=row_separator
                )

            #                          #
            # --- POST-RENDER AREA --- #
            #                          #
            print(pre_table)

    def demo(self):
        """Demonstration function."""
        input('--- Press ENTER to see the dataset as is ---\n')
        print(dataset)
        input(
            '\n--- Now press ENTER to see a dataset reapeated '
            '1000 times renderized by Outfancy ---\n'
            )
        self.render(1000 * dataset)

    def get_final_order_list(self, order_list=None, data=None):
        """
        It takes the original order and get the final order list,
        data will be rearranged taking as parameter only this final
        order_list. (This avoid multiple rearranging).
        """

        # Check if order_list was provided, if not, return an error.
        if not isinstance(order_list, list):
            return '--- LargeTable > get_final_order_list: order_list '\
                   'was not received or it is not valid. ---'

        # Check if data was provided, if not, return an error.
        if data is None:
            return '--- LargeTable > get_final_order_list: '\
                   'data was not received. ---'

        # If data have no rows, empty order will be returned.
        if len(data) < 1:
            return []

        # It generates the base_list with a len of data[0].
        base_list = [x for x in range(len(data[0]))]

        # It rearrange values in base_list based in values of order_list.
        for element in order_list:
            # It generates the new_list.
            new_list = []
            for x in element:
                if widgets.index_is_in_list(the_list=base_list, index=x):
                    new_list.append(base_list[x])
            # base_list is now the finished new_list.
            base_list = new_list

    def rearrange_row(self, row=None, order=None):
        """
        It rearranges a row based on provided order.
        """
        # Check if row was provided, if not, return an error.
        if row is None:
            return '--- LargeTable > get_final_order_list:'\
                   'data_to_analyze was not received. ---'

        # If order was not provided or if is not a list,
        # row will be returned without rearrange.
        if not isinstance(order, list):
            return row

        rearranged_row = []
        for element in order:
            if widgets.index_is_in_list(the_list=row, index=element):
                rearranged_row.append(row[element])

        # The rearranged row is returned.
        return row
