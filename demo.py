#!/usr/bin/env python3

from time import sleep

import outfancy.table
from outfancy.example_dataset import color_dataset, dataset


def demo():
    """Function that run all demonstrations."""
    print('--- STARTING THE DEMO ---')
    sleep(2)

    print('· Test table printing (only providing dataset).')
    sleep(2)
    test_table()
    sleep(4)
    print('#' * 60)

    print('· Test table printing with colors '
          '(the colors are provided by user in the dataset).')
    sleep(2)
    test_table_with_colors()
    sleep(4)
    print('#' * 60)

    print('· Test of an Oneline object.')
    sleep(2)
    test_oneline()
    sleep(4)
    print('#' * 60)

    print(
        '· Test of a Table object, customized to '
        'show how the parameters works.'
        )
    sleep(2)
    test_customized_table()
    sleep(4)
    print('#' * 60)

    print('· Test of a table object, to show how works width without'
          'automatical assignement deactivated.'
          )
    sleep(2)
    test_table_width_false()
    sleep(4)
    print('#' * 60)


def create_objects():
    # It creates the object that render Tables.
    global table
    table = outfancy.table.Table()
    # It creates the object that is configured to print one line each time.
    global oneline_table
    oneline_table = outfancy.table.Oneline()


def test():
    """Test included with outfancy.table.Table"""
    input('--- Press ENTER to see the dataset as is ---')
    print(dataset)
    input(
        '--- Now press ENTER to see the dataset renderized by Outfancy ---'
        )
    create_objects()
    print(table.render(dataset))


def test_table():
    """# Test table (the same result as test())."""
    print('>>> import outfancy')
    print('>>> table = outfancy.table.Table()')
    print(f'>>> dataset = {dataset}')
    print('>>> print(table.render(dataset))')
    sleep(2)
    create_objects()
    print(table.render(dataset))


def test_table_with_colors():
    """Test table with_colors."""
    print('>>> import outfancy')
    print('>>> table = outfancy.table.Table()')
    print(f'>>> color_dataset = {color_dataset}')
    print('>>> print(table.render(color_dataset))')
    sleep(2)
    create_objects()
    print(table.render(color_dataset))


def test_oneline():
    """Test of an Oneline object."""
    print('>>> import outfancy')
    print('>>> oneline_table = outfancy.table.Oneline()')
    print(f'>>> dataset = {dataset}')
    print('>>> for x in range(10):')
    print('>>>     sleep(1)')
    print(">>>     print('=' * 60")
    print('>>>     print(oneline_table.render(dataset[x]))')
    sleep(2)
    create_objects()
    for x in range(10):
        sleep(1)
        print('=' * 60)
        print(oneline_table.render(dataset[x]))


def test_customized_table():
    """
    Test of a Table object, customized to show how the parameters works.
    """
    print('>>> import outfancy')
    print('>>> table = outfancy.table.Table()')
    print(">>> separator = '|'")
    print(f'>>> dataset = {dataset}')
    print(">>> label_list = ['Id' 'Company', 'Added date', 'Added hour',")
    print("    'Last edition', 'Last edition', 'Value', 'Description']")
    print('>>> order = [0, 1, 6, 7]')
    print('>>> width = [2, 20, 15, 12]')
    print('>>> print(table.render(dataset, separator, order, width=width))')
    sleep(2)
    create_objects()
    separator = '-|-'
    label_list = ['Id' 'Company', 'Value', 'Description']
    order = [0, 1, 6, 7]
    width = [2, 20, 15, 12]
    print(table.render(dataset, separator, label_list, order, width=width))


def test_table_width_false():
    """
    Test of a table object, to show how works width
    without automatical assignement deactivated.
    """
    print('>>> import outfancy')
    print('>>> table = outfancy.table.Table()')
    print(f'>>> dataset = {dataset}')
    print('>>> print(table.render(dataset, width=False))')
    sleep(2)
    create_objects()
    print(table.render(dataset, width=False))
    sleep(2)
    print(' --- TEST NOTE: With width=False, Outfancy '
          'will asign the same width to all columns.')


if __name__ == '__main__':
    demo()
