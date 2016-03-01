#!/usr/bin/python3
# -*- coding: utf-8 -*-

import outfancy

from time import sleep

def create_motors():
    # It creates the object that render Tables.
    global motor 
    motor = outfancy.render.Table()
    # It creates the object that is configured to print one line each time.
    global motor_oneline 
    motor_oneline = outfancy.render.Oneline()

# It defines the recordset, a set of data prepared for test purposes.
recordset = [(1, 'Feisbuk', '18-10-2015', '21:57:17', '18-10-2015', '21:57:17', 1234, 'Social network bla bla bla used by people bla bla.'), (2, 'Gugle', '18-10-2015', '21:57:44', '18-10-2015', '21:57:44', 12323, 'Search engine that categorize results using an algorithm that bla bla bla.'), (3, 'Opera', '18-10-2015', '21:58:39', '18-10-2015', '21:58:39', 4324, 'Navegador de internerd, también es una disciplina musical, que, valga la redundancia, requiere de una brutal disciplina por parte de los interpretes.'), (4, 'Audi', '18-10-2015', '21:59:51', '18-10-2015', '21:59:51', 0, 'OOOO <-- Fabricante alemán de vehiculos de alta gama.'), (5, 'The Simpsons', '18-10-2015', '22:0:44', '18-10-2015', '22:0:44', 0, 'Una sitcom que lleva veintipico de temporadas, si no la viste, se puede presumir que vivís bajo una piedra.'), (6, 'BMW', '18-10-2015', '22:1:18', '18-10-2015', '22:1:18', 98765, 'Fabricante alemán de autos de lujo.'), (7, 'Yahoo', '18-10-2015', '22:1:56', '18-10-2015', '22:1:56', 53430, 'Expresión de alegría, o compañía gringolandesa.'), (8, 'Coca Cola', '18-10-2015', '22:3:19', '18-10-2015', '22:3:19', 200, 'Compañía que fabrica bebidas, y que no nos paga por ponerla en py-test :c.'), (9, 'Pepsi', '18-10-2015', '22:3:40', '18-10-2015', '22:3:40', 340, 'Competidora de la anterior compañía mencionada, y que tampoco nos paga :c.'), (10, 'GitHub', '18-10-2015', '22:4:42', '18-10-2015', '22:4:42', 563423, 'Plataforma de gestión de co0o0o0ó0digo.'), (11, 'Johnny Walker', '18-10-2015', '22:5:34', '18-10-2015', '22:5:34', 4252, 'Whisky escocés.'), (12, 'Mercury', '18-10-2015', '22:5:51', '18-10-2015', '22:5:51', 23423, 'Fabricante de motores fuera de borda.'), (13, 'Rolls Royce', '18-10-2015', '22:6:7', '18-10-2015', '22:6:7', 75832, 'Fabricante de motores para aviones, y autos de alta gama.')]

# Test included with Outfancy.
def test():
    input('--- Press ENTER to see the recordset as is ---')
    print(recordset)
    input('--- Now press ENTER to see the recordset renderized by Outfancy ---')
    create_motors()
    print(motor.render(recordset))

# Test table (the same result as test())
def test_table():
    print('>>> import outfancy')
    print('>>> motor = outfancy.render.Table()')
    print('>>> recordset =', recordset)
    print('>>> print(motor.render(recordset))')
    sleep(2)
    create_motors()
    print(motor.render(recordset))

# Test of an Oneline object.
def test_oneline():
    print('>>> import outfancy')
    print('>>> motor_oneline = outfancy.render.Oneline()')
    print('>>> recordset =', recordset)
    print('>>> for x in range(10):')
    print('>>>     sleep(1)')
    print(">>>     print('#' * 60")
    print('>>>     print(motor_oneline.render(recordset[x]))')
    sleep(2)
    create_motors()
    for x in range(10):
        sleep(1)
        print('#' * 60)
        print(motor_oneline.render(recordset[x]))

# Test of a Table object, configured to show errors.
def test_table_show_errors():
    print('>>> import outfancy')
    print('>>> motor = outfancy.render.Table()')
    print('>>> motor.set_show_errors(True)')
    print('>>> recordset =', recordset)
    print('>>> print(motor.render(recordset))')
    sleep(2)
    create_motors()
    motor.set_show_errors(True)
    print(motor.render(recordset))

# Test of a Table object, configured to show errors.
def test_table_show_errors():
    print('>>> import outfancy')
    print('>>> motor = outfancy.render.Table()')
    print('>>> motor.set_show_errors(True)')
    print('>>> recordset =', recordset)
    print('>>> print(motor.render(recordset))')
    sleep(2)
    create_motors()
    motor.set_show_errors(True)
    print(motor.render(recordset))

# Test of a Table object, customized to show how the parameters works.
def test_customized_table():
    print('>>> import outfancy')
    print('>>> motor = outfancy.render.Table()')
    print('>>> motor.set_show_errors(True)')
    print(">>> separator = '|'")
    print('>>> recordset =', recordset)
    print(">>> label_list = ['Id' 'Company', 'Added date', 'Added hour' ,'Last edition', 'Last edition', 'Value', 'Description']")
    print('>>> order = [0, 1, 6, 7]')
    print('>>> width = [2, 20, 15, 12]')
    print('>>> print(motor.render(recordset, separator, order, width=width))')
    sleep(2)
    create_motors()
    motor.set_show_errors(True)
    separator = '-|-'
    label_list = ['Id' 'Company', 'Value', 'Description']
    order = [0, 1, 6, 7]
    width = [2, 20, 15, 12]
    print(motor.render(recordset, separator, label_list, order, width=width))

# Test of a table object, to show how works width without automatical assignement deactivated.
def test_table_width_false():
    print('>>> import outfancy')
    print('>>> motor = outfancy.render.Table()')
    print('>>> motor.set_show_errors(True)')
    print('>>> recordset =', recordset)
    print('>>> print(motor.render(recordset, width=False))')
    sleep(2)
    create_motors()
    motor.set_show_errors(True)
    print(motor.render(recordset, width=False))
    sleep(2)
    print(' --- TEST NOTE: With width=False, Outfancy will asign the same width to all columns.')
