from time import sleep

import outfancy.table
from outfancy.example_dataset import color_dataset, dataset


def demo():
    """Run all demonstrations."""
    print('--- STARTING THE DEMO ---')
    sleep(1)

    print('· Table printing (only providing dataset).')
    sleep(1)
    test_table()
    sleep(2)
    print('#' * 60)

    print('· Table printing with colors '
          '(colors are provided by the user in the dataset).')
    sleep(1)
    test_table_with_colors()
    sleep(2)
    print('#' * 60)

    print('· Oneline object.')
    sleep(1)
    test_oneline()
    sleep(2)
    print('#' * 60)

    print('· Customized Table object.')
    sleep(1)
    test_customized_table()
    sleep(2)
    print('#' * 60)

    print('· Table with width=False (equal width for all columns).')
    sleep(1)
    test_table_width_false()
    sleep(2)
    print('#' * 60)


def test_table():
    """Test basic table rendering."""
    print('>>> import outfancy')
    print('>>> table = outfancy.table.Table()')
    print(f'>>> dataset = {dataset}')
    print('>>> print(table.render(dataset))')
    sleep(1)
    table = outfancy.table.Table()
    print(table.render(dataset))


def test_table_with_colors():
    """Test table with ANSI colors in the dataset."""
    print('>>> import outfancy')
    print('>>> table = outfancy.table.Table()')
    print(f'>>> color_dataset = {color_dataset}')
    print('>>> print(table.render(color_dataset))')
    sleep(1)
    table = outfancy.table.Table()
    print(table.render(color_dataset))


def test_oneline():
    """Test real-time single-line rendering with Oneline."""
    print('>>> import outfancy')
    print('>>> oneline_table = outfancy.table.Oneline()')
    print(f'>>> dataset = {dataset}')
    print('>>> for x in range(10):')
    print('>>>     sleep(1)')
    print(">>>     print('=' * 60)")
    print('>>>     print(oneline_table.render(dataset[x]))')
    sleep(1)
    oneline_table = outfancy.table.Oneline()
    for x in range(10):
        sleep(1)
        print('=' * 60)
        print(oneline_table.render(dataset[x]))


def test_customized_table():
    """Test Table with custom separator, column order, and explicit widths."""
    separator = '-|-'
    label_list = ['Id', 'Company', 'Value', 'Description']
    order = [0, 1, 6, 7]
    width = [2, 20, 15, 12]
    print('>>> import outfancy')
    print('>>> table = outfancy.table.Table()')
    print(f">>> separator = '{separator}'")
    print(f'>>> dataset = {dataset}')
    print(f'>>> label_list = {label_list}')
    print(f'>>> order = {order}')
    print(f'>>> width = {width}')
    print('>>> print(table.render(dataset, separator, label_list, order, width=width))')
    sleep(1)
    table = outfancy.table.Table()
    print(table.render(dataset, separator, label_list, order, width=width))


def test_table_width_false():
    """Test Table with width=False (equal width assigned to all columns)."""
    print('>>> import outfancy')
    print('>>> table = outfancy.table.Table()')
    print(f'>>> dataset = {dataset}')
    print('>>> print(table.render(dataset, width=False))')
    sleep(1)
    table = outfancy.table.Table()
    print(table.render(dataset, width=False))
    sleep(1)
    print('--- NOTE: With width=False, Outfancy assigns equal width to all columns.')
