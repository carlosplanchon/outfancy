#!/usr/bin/python3
# -*- coding: utf-8 -*-

import outfancy

recordset = [(1, 'Google', '18-10-2015', '21:56:51', '18-10-2015', '21:56:51', 0, ''), (2, 'Feisbuk', '18-10-2015', '21:57:17', '18-10-2015', '21:57:17', 0, 'Red social bla bla bla utilizada gente bla bla'), (3, 'Gugle', '18-10-2015', '21:57:44', '18-10-2015', '21:57:44', 0, 'Motor de busqueda que categoriza resultados por links bla bla'), (4, 'Opera', '18-10-2015', '21:58:39', '18-10-2015', '21:58:39', 0, 'Navegador de internerd, también es una disciplina musical, que, valga la redundancia, requiere de una brutal disciplina por parte de los interpretes.'), (5, 'Audi', '18-10-2015', '21:59:51', '18-10-2015', '21:59:51', 0, 'OOOO <-- Fabricante alemán de vehiculos de alta gama'), (6, 'The Simpsons', '18-10-2015', '22:0:44', '18-10-2015', '22:0:44', 0, 'Una sitcom que lleva veintipico de temporadas, si no la viste, se puede presumir que vivís bajo una piedra.'), (7, 'BMW', '18-10-2015', '22:1:18', '18-10-2015', '22:1:18', 0, 'Fabricante alemán de autos de lujo'), (8, 'Yahoo', '18-10-2015', '22:1:56', '18-10-2015', '22:1:56', 0, 'Expresión de alegría, o compañía gringolandesa.'), (9, 'Coca Cola', '18-10-2015', '22:3:19', '18-10-2015', '22:3:19', 0, 'Compañía que fabrica bebidas, y que no nos paga por ponerla en py-test :c'), (10, 'Pepsi', '18-10-2015', '22:3:40', '18-10-2015', '22:3:40', 0, 'Competidora de la anterior compañía mencionada, y que tampoco nos paga :c'), (11, 'GitHub', '18-10-2015', '22:4:42', '18-10-2015', '22:4:42', 0, 'Plataforma de gestión de co0o0o0ó0digo'), (12, 'Johnny Walker', '18-10-2015', '22:5:34', '18-10-2015', '22:5:34', 0, 'Whisky escocés'), (13, 'Mercury', '18-10-2015', '22:5:51', '18-10-2015', '22:5:51', 0, 'Fabricante de motores para lanchas'), (14, 'Rolls Royce', '18-10-2015', '22:6:7', '18-10-2015', '22:6:7', 0, 'Fabricante de motores para aviones, y autos de alta gama')]

input('--- Presione ENTER para ver el recordset tal cual es ---')
print(recordset)
input('--- Ahora presione ENTER para ver el recordset renderizado por Outfancy ---')

outfancy.render.render_recordset(recordset)
