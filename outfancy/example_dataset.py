#!/usr/bin/env python3

dataset = [
        (
            1,
            'Feisbuk',
            '18-10-2015',
            '21:57:17',
            '18-10-2015',
            '21:57:17',
            1234,
            'Social network bla bla bla used by people bla bla.'
        ),
        (
            2,
            'Gugle',
            '18-10-2015',
            '21:57:44',
            '18-10-2015',
            '21:57:44',
            12323,
            'Search engine that categorize results using '
            'an algorithm that bla bla bla.'
        ),
        (
            3,
            'Opera',
            '18-10-2015',
            '21:58:39',
            '18-10-2015',
            '21:58:39',
            4324,
            'Navegador de internerd, también es una disciplina '
            'musical, que, valga la redundancia, requiere de una '
            'brutal disciplina por parte de los interpretes.'
        ),
        (
            4,
            'Audi',
            '18-10-2015',
            '21:59:51',
            '18-10-2015',
            '21:59:51',
            0,
            'OOOO <-- Fabricante alemán de vehiculos de alta gama.'
        ),
        (
            5,
            'The Simpsons',
            '18-10-2015',
            '22:0:44',
            '18-10-2015',
            '22:0:44',
            0,
            'Una sitcom que lleva veintipico de temporadas, si no '
            'la viste se puede asumir que vivís bajo una piedra.'
        ),
        (
            6,
            'BMW',
            '18-10-2015',
            '22:1:18',
            '18-10-2015',
            '22:1:18',
            98765,
            'Fabricante alemán de autos de lujo.'
        ),
        (
            7,
            'Yahoo',
            '18-10-2015',
            '22:1:56',
            '18-10-2015',
            '22:1:56',
            53430,
            'Expresión de alegría, o compañía gringolandesa.'
        ),
        (
            8,
            'Coca Cola',
            '18-10-2015',
            '22:3:19',
            '18-10-2015',
            '22:3:19',
            200,
            'Compañía que fabrica bebidas, y que no nos paga '
            'por ponerla en py-test :c.'
        ),
        (
            9,
            'Pepsi',
            '18-10-2015',
            '22:3:40',
            '18-10-2015',
            '22:3:40',
            340,
            'Competidora de la anterior compañía mencionada, y '
            'que tampoco nos paga :c.'
        ),
        (
            10,
            'GitHub',
            '18-10-2015',
            '22:4:42',
            '18-10-2015',
            '22:4:42',
            563423,
            'Plataforma de gestión de co0o0o0ó0digo.'
        ),
        (
            11,
            'Johnny Walker',
            '18-10-2015',
            '22:5:34',
            '18-10-2015',
            '22:5:34',
            4252,
            'Whisky escocés.'
        ),
        (
            12,
            'Mercury',
            '18-10-2015',
            '22:5:51',
            '18-10-2015',
            '22:5:51',
            23423,
            'Fabricante de motores fuera de borda.'
        ),
        (
            13,
            'Rolls Royce',
            '18-10-2015',
            '22:6:7',
            '18-10-2015',
            '22:6:7',
            75832,
            'Fabricante de motores para aviones '
            'y autos de alta gama.'
        )
    ]


color_dataset = [
        (
            1,
            'Feisbuk',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '21:57:17',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '21:57:17',
            1234,
            'Social network bla bla bla used by people bla bla.'
        ),
        (
            2,
            'Gugle',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '21:57:44',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '21:57:44',
            12323,
            'Search engine that categorize results using '
            'an algorithm that bla bla bla.'
        ),
        (
            3,
            'Opera',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '21:58:39',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '21:58:39',
            4324,
            'Navegador de internerd, también es una disciplina '
            'musical, que, valga la redundancia, requiere de una '
            'brutal disciplina por parte de los interpretes.'
        ),
        (
            4,
            'Audi',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '21:59:51',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '21:59:51',
            0,
            'OOOO <-- Fabricante alemán de vehiculos de alta gama.'
        ),
        (
            5,
            'The Simpsons',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '22:0:44',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '22:0:44',
            0,
            'Una sitcom que lleva veintipico de temporadas, si no '
            'la viste se puede asumir que vivís bajo una piedra.'
        ),
        (
            6,
            'BMW',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '22:1:18',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '22:1:18',
            98765,
            'Fabricante alemán de autos de lujo.'
        ),
        (
            7,
            'Yahoo',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '22:1:56',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '22:1:56',
            53430,
            'Expresión de alegría, o compañía gringolandesa.'
        ),
        (
            8,
            'Coca Cola',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '22:3:19',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '22:3:19',
            200,
            'Compañía que fabrica bebidas, y que no nos paga '
            'por ponerla en py-test :c.'
        ),
        (
            9,
            'Pepsi',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '22:3:40',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '22:3:40',
            340,
            'Competidora de la anterior compañía mencionada, y '
            'que tampoco nos paga :c.'
        ),
        (
            10,
            'GitHub',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '22:4:42',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '22:4:42',
            563423,
            'Plataforma de gestión de co0o0o0ó0digo.'
        ),
        (
            11,
            'Johnny Walker',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '22:5:34',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '22:5:34',
            4252,
            'Whisky escocés.'
        ),
        (
            12,
            'Mercury',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '22:5:51',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '22:5:51',
            23423,
            'Fabricante de motores fuera de borda.'
        ),
        (
            13,
            'Rolls Royce',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '22:6:7',
            '\x1b[1;32m18-10-2015\x1b[0;39m',
            '22:6:7',
            75832,
            'Fabricante de motores para aviones, y autos de alta gama.'
        )
    ]
