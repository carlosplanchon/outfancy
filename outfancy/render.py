#!/usr/bin/python3
# -*- coding: utf-8 -*-

from . import widgets

# Chequeo inicial.
widgets.check_inicio()

class Recordset:
    '''Recordset permite renderizar en buen formato las salidas de un recordset, 
    para esto es recomendable usar objeto.render(DATOS)'''
    def __init__(self):
        # Check_data especifica si debe chequearse o no la informacion del recordset. 
        self.check_data = True
        # Corrector = Indica el valor de correcion a aplicar en el eje x (margen en blanco a la derecha. de la pantalla).
        self.corrector = -2
        # Alto maximo que puede tener una tupla en pantalla.
        self.max_y_cuadro_threshold = 20
        # Threshold de analisis al reconstruir datos de screen.lista_tipo_datos.
        self.analyze_threshold = 10
        # Con esta opcion los errores se muestran en pantalla luego de la impresion.
        self.show_errores = True
        # Se especifica si se registran o no errores en el log del programa.
        self.log_errores = True
        # El ancho minimo que puede tener una columna antes de que se deje de mostrar.
        self.show_ancho_thresholding = 5

    def set_check_data(self, x = True):
        self.check_data = x

    def set_corrector(self, x = -2):
        self.corrector = x

    def set_max_y_cuadro_threshold(self, x = 20):
        self.max_y_cuadro_threshold = x

    def set_analyze_threshold(self, x = 10):
        self.analyze_threshold = x

    def set_show_errores(self, x = True):
        self.show_errores = x

    def set_log_errores(self, x = True):
        self.log_errores = x

    def set_show_ancho_thresholding(self, x = True):
        self.show_ancho_thresholding = x

    def show_check_data(self):
        print(self.check_data)

    def show_corrector(self):
        print(self.corrector)

    def show_max_y_cuadro_threshold(self):
        print(self.max_y_cuadro_threshold)

    def show_analyze_threshold(self):
        print(self.analyze_threshold)

    def show_show_errores(self):
        print(self.show_errores)

    def show_log_errores(self):
        print(self.log_errores)

    def show_show_ancho_thresholding(self):
        print(self.show_ancho_thresholding)

    def render(self, data = None, separador = None, lista_etiquetas = None, orden = None, lista_tipo_datos = None, cadena_prioridades = None):
        """
        Render recibe seis (6) parametros, y se encarga de renderizar
        un recordset (respuestas a consultas SQL en bases de datos), de manera organizada.

        Parametros:
        data: Se debe especificar un recordset Ej: [('a','b','c'),('d','e','f')].
        separador: Permite modificar la cadena que separa las columnas, por defecto es un espacio en blanco " ".
        lista_etiquetas: Permite modificar la lista de etiquetas que aparece sobre la tabla renderizada.
            Si lista_etiquetas es None el programa generara etiquetas en base a lista_tipo_datos.
        orden: Permite modificar el orden en el cual se muestran las columnas, suprimiendo estas inclusive.
        lista_tipo_datos: Permite modificar el tipo de datos que el sistema de render asigna a una columna.
            Si no se especifica, el programa intentara averiguar que tipo de datos tiene cada columna.
        cadena_prioridades: Permite modificar la prioridad que se le asigna a cada columna, si no se especifica
        el programa asignara prioridades en base a lista_tipo_datos.
        Si el espacio para mostrar las columnas no es suficiente, el programa podra suprimir columnas
        (iniciando por las de baja prioridad).
        """
        # Setea el registro interno de errores a 0.
        global errores
        errores = []
        ###############################################
        # --- CHEQUEOS DE INTEGRIDAD EN LOS DATOS --- #
        ###############################################
        # --- Se chequea la existencia de los datos --- #
        if data == None:
            return '--- Recordset > Render: No se han recibido datos para imprimir ---'

        # --- Si en configuracion se especifica, Se chequea la integridad de los datos --- #
        if self.check_data:
            if check_data_integrity(data):
                return '--- Render > check_data_integrity: Dato invalido o no integro ---'

        ##############################
        # --- AREA DE PRE-RENDER --- #
        ##############################
        # --- Se analizan las dimensiones de la pantalla --- #
        screen_x, screen_y = widgets.medir_dimensiones()
        # --- Se aplica valor de correccion a screen_x --- #
        screen_x += self.corrector
        # --- Se chequea el separador --- #
        separador = check_separador(separador, screen_x)
        # --- Se chequea la validez del orden provisto --- #
        orden = check_orden(data, orden)
        # --- Se reordenan los datos y las etiquetas --- #
        ordered_data = reordenar_datos(data, orden)
        # --- Chequea la longitud maxima para mostrar cada campo de ordered_data --- #
        maximo = check_maximos(ordered_data)
        # --- Se chequea la integridad de la lista de tipos de datos --- #
        lista_tipo_datos = check_lista_tipo_datos_integrity(self.analyze_threshold, data, lista_tipo_datos)
        # --- Se reordena lista_tipo_datos --- #
        ordered_lista_tipo_datos = reordenar_lista_tipo_datos(lista_tipo_datos, orden)
        ##########################
        # --- AREA DE RENDER --- #
        ##########################
        # --- Asigna el ancho para mostrar las columnas, si este no es provisto, intenta deducirlo --- #
        ordered_lista_tipo_datos, cadena_prioridades, ancho = asign_ancho_columnas(self.show_ancho_thresholding, maximo, screen_x, ordered_lista_tipo_datos, cadena_prioridades, len(separador), orden)
        # --- Genera las casillas que contienen los datos --- #
        linea_cuadros = generar_cuadros_pantalla(self.max_y_cuadro_threshold, ordered_data, ancho, maximo, screen_y)
        # --- Genera el area de la pantalla que contiene el pre_render del recordset --- #
        pantalla = generar_pantalla(linea_cuadros, separador)
        # --- Chequea que la lista de etiquetas este en orden, si no es asi intenta deducirlas --- #
        lista_etiquetas = check_lista_etiquetas(lista_etiquetas, lista_tipo_datos, ancho, orden, separador)
        ###############################
        # --- AREA DE POST-RENDER --- #
        ###############################
        # --- Lleva a cabo el post_render, uniendo el pre_render del recordset con los demas datos --- #
        return post_render(self.show_errores, self.log_errores, pantalla, lista_etiquetas, len(separador))


    def test(self):
        recordset = [(1, 'Feisbuk', '18-10-2015', '21:57:17', '18-10-2015', '21:57:17', 1234, 'Red social bla bla bla utilizada gente bla bla'), (2, 'Gugle', '18-10-2015', '21:57:44', '18-10-2015', '21:57:44', 12323, 'Motor de busqueda que categoriza resultados por links bla bla'), (3, 'Opera', '18-10-2015', '21:58:39', '18-10-2015', '21:58:39', 4324, 'Navegador de internerd, también es una disciplina musical, que, valga la redundancia, requiere de una brutal disciplina por parte de los interpretes.'), (4, 'Audi', '18-10-2015', '21:59:51', '18-10-2015', '21:59:51', 0, 'OOOO <-- Fabricante alemán de vehiculos de alta gama'), (5, 'The Simpsons', '18-10-2015', '22:0:44', '18-10-2015', '22:0:44', 0, 'Una sitcom que lleva veintipico de temporadas, si no la viste, se puede presumir que vivís bajo una piedra.'), (6, 'BMW', '18-10-2015', '22:1:18', '18-10-2015', '22:1:18', 98765, 'Fabricante alemán de autos de lujo'), (7, 'Yahoo', '18-10-2015', '22:1:56', '18-10-2015', '22:1:56', 53430, 'Expresión de alegría, o compañía gringolandesa.'), (8, 'Coca Cola', '18-10-2015', '22:3:19', '18-10-2015', '22:3:19', 200, 'Compañía que fabrica bebidas, y que no nos paga por ponerla en py-test :c'), (9, 'Pepsi', '18-10-2015', '22:3:40', '18-10-2015', '22:3:40', 340, 'Competidora de la anterior compañía mencionada, y que tampoco nos paga :c'), (10, 'GitHub', '18-10-2015', '22:4:42', '18-10-2015', '22:4:42', 563423, 'Plataforma de gestión de co0o0o0ó0digo'), (11, 'Johnny Walker', '18-10-2015', '22:5:34', '18-10-2015', '22:5:34', 4252, 'Whisky escocés'), (12, 'Mercury', '18-10-2015', '22:5:51', '18-10-2015', '22:5:51', 23423, 'Fabricante de motores para lanchas'), (13, 'Rolls Royce', '18-10-2015', '22:6:7', '18-10-2015', '22:6:7', 75832, 'Fabricante de motores para aviones, y autos de alta gama')]
        input('--- Presione ENTER para ver el recordset tal cual es ---')
        print(recordset)
        input('--- Ahora presione ENTER para ver el recordset renderizado por Outfancy ---')
        print(self.render(recordset))

#####################
#                   #
# --- FUNCIONES --- #
#                   #
#####################

letras = 'abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ'

def post_render(show_errores = True, log_errores = True, pantalla = None, lista_etiquetas = None, len_separador = None):
    # Si no se provee pantalla.
    if pantalla == None:
        errores.append('Render > post_render: No se proveyo pantalla, esto pasa si los datos no son validos.')
        print('Render > post_render: Datos invalidos')

    # Si separador no es provisto, genera uno y emite un error.
    if len_separador == None:
        errores.append('Render > post_render: No se proveyo separador.')
        len_separador = 1

    # Si lista_etiquetas no es provista, se asigna una cadena vacia.
    if lista_etiquetas == None:
        errores.append('Render > post_render: No se proveyo lista_etiquetas.')
        lista_etiquetas = ''

    # Variable que almacena la tabla renderizada.
    post_renderizado = ''

    # Esta funcion se encarga de imprimir la pantalla junto con las etiquetas.
    post_renderizado += '\x1b[1;33m' + lista_etiquetas + '\x1b[0;99m'+ pantalla + '\x1b[0;99m\n'
    # Si en la configuracion se especifica que se debe mostrar errores.
    if show_errores and len(errores) > 0:
        post_renderizado += '\n ' + ' ' * (len_separador - 1) + '\x1b[1;36mRender > Errores > ' + widgets.fecha_actual() + ' ' + widgets.hora_actual() + '\x1b[0;91m\n'
        for x in range(len(errores)): 
            post_renderizado += ' ' * len_separador + errores[x] + '\n'
        post_renderizado += '\x1b[0;99m'

    # Si en la configuracion se especifica que se deben registrar los errores.
    if log_errores:
        widgets.write_log('Render > Errores > ' + widgets.fecha_actual() + ' ' + widgets.hora_actual() + ' -\n' + '\n'.join(errores))

    return post_renderizado

# Esta funcion chequea que la lista de etiquetas este en orden, si no es asi intenta reconstruirla.
def check_lista_etiquetas(lista_etiquetas = None, lista_tipo_datos = None, ancho = None, orden = None, separador = None):
    # Lista de elementos que deben intentar ser reconstruidos #
    to_rebuild = []
    # Si lista etiquetas es invalida, se reconstruye.
    if type(lista_etiquetas) != list:
        errores.append('Render > check_lista_etiquetas: lista_etiquetas no fue provista o es invalida.')
        lista_etiquetas = []
        for x in range(len(lista_tipo_datos)):
            lista_etiquetas.append(None)

    for x in range(len(lista_etiquetas)):
        if type(lista_etiquetas[x]) != str or lista_etiquetas[x] == None:
            to_rebuild.append(x)
            lista_etiquetas[x] = None

    if separador == None:
        errores.append('Render > check_lista_etiquetas: No se proveyo separador.')
        separador = ' '

    # Si la lista de etiquetas tiene mas elementos que elementos lista_tipo_datos, lista_etiquetas se recorta.
    if len(lista_etiquetas) > len(lista_tipo_datos):
        lista_etiquetas = lista_etiquetas[0:len(lista_tipo_datos)]
        errores.append('Render > check_lista_etiquetas_integrity: Fue necesario acortar lista_etiquetas.')
    # Si es menor, se agrega None a lista_etiquetas.
    elif len(lista_etiquetas) < len(lista_tipo_datos):
        errores.append('Render > check_lista_etiquetas_integrity: lista_etiquetas es muy corta.')
        for x in range(len(lista_etiquetas),len(lista_tipo_datos)):
            lista_etiquetas.append(None)
            to_rebuild.append(x)

    # Para cada elemento de lista_etiquetas que necesita reconstruccion.
    for x in to_rebuild:
        # Se intenta reconstruir lista_etiquetas.
        if lista_tipo_datos[x] == 'id':
            etiqueta = 'Id'
        elif lista_tipo_datos[x] == 'name':
            etiqueta = 'Nombre'
        elif lista_tipo_datos[x] == 'date':
            etiqueta = 'Fecha'
        elif lista_tipo_datos[x] == 'time':
            etiqueta = 'Hora'
        elif lista_tipo_datos[x] == 'value':
            etiqueta = 'Valor'
        elif lista_tipo_datos[x] == 'desc':
            etiqueta = 'Descripción'
        else:
            etiqueta = ''

        # Se asigna el tipo averiguado a la lista_tipo_datos
        lista_etiquetas[x] = etiqueta

    if len(to_rebuild) > 0:
        errores.append('Render > check_lista_etiquetas: Fue necesario reconstruir lista_etiquetas.')

    if orden == None or type(orden) != list:
        errores.append('Render > check_lista_etiquetas: No se proveyo orden o este es invalido.')
        ordered_lista_etiquetas = lista_etiquetas
    else:
        ordered_lista_etiquetas = []
        for elemento in orden:
            try:
                ordered_lista_etiquetas.append(lista_etiquetas[int(elemento)])
            except:
                errores.append('Render > check_lista_etiquetas: Error al intentar reordenar las etiquetas.')

    # Si no se proveen anchos, se emite un error y se retorna lista_etiquetas.
    if ancho == None:
        errores.append('Render > check_lista_etiquetas: No se proveyo lista ancho (lista de anchos).')
        return separador + separador.join(ordered_lista_etiquetas)

    # Para cada elemento en la longitud de lista anchos.
    for x in range(len(ancho)):
        # Si la etiqueta es mayor al ancho de la columna.
        if len(ordered_lista_etiquetas[x]) > ancho[x]:
            ordered_lista_etiquetas[x] = ordered_lista_etiquetas[x][0:ancho[x]]
        # Si la etiqueta es menor.
        elif len(ordered_lista_etiquetas[x]) < ancho[x]:
            ordered_lista_etiquetas[x] = ordered_lista_etiquetas[x] + ' ' * (ancho[x] - len(ordered_lista_etiquetas[x]))

    # Se retorna ordered_lista_etiquetas.
    return separador + separador.join(ordered_lista_etiquetas)


# Esta funcion une las casillas intercalandoles el separador.
def generar_pantalla(linea_cuadros = None, separador = None):
    if linea_cuadros == None:
        return 'Render > generar_pantalla: No se proveyo linea_cuadros.'

    if separador == None:
        errores.append('Render > generar_pantalla: No se proveyo separador.')
        separador = ' '

    pre_pantalla = ''
    # --- Para cada tupla de linea_cuadros. --- #
    for tupla in linea_cuadros:
        if len(tupla) > 0:
            for linea in range(len(tupla[0])):
                pre_pantalla += '\n'
                # --- Para cada cuadro se retirara una linea --- #
                for cuadro in tupla:
                    pre_pantalla += separador + cuadro[linea]

    return pre_pantalla


def generar_cuadros_pantalla(max_y_cuadro_threshold = 20, ordered_data = None, ancho = None, maximo = None, screen_y = None):
    # --- Si no se proveen datos, retorna una lista vacia --- #
    if ordered_data == None:
        errores.append('Render > generar_cuadros: No se proveyo ordered_data.')
        return []

    # --- Si no se provee ancho de columnas, se retorna una lista vacia --- #
    if ancho == None:
        errores.append('Render > generar_cuadros: No se proveyo ancho_columnas.')
        return []

    # --- Si no se provee ancho de columnas, se retorna una lista vacia --- #
    if maximo == None:
        errores.append('Render > generar_cuadros: No se proveyo maximo[].')
        return []

    # Lineas pantalla guarda las lineas que seran generadas.
    linea_cuadros = []
    for tupla in range(len(ordered_data)):
        # Se analiza cada columna de la tupla
        cuadros_a_insertar = []
        for columna in range(len(ancho)):
            # --- Se genera un cuadro --- #
            after = ancho[columna]
            cuadro = []
            cuadro_a_recortar = str(ordered_data[tupla][columna])
            # --- Si cuadro_a_recortar y ancho[columna] son iguales, se appendea el cuadro sin mas --- #
            if len(cuadro_a_recortar) == ancho[columna]:
                cuadro.append(cuadro_a_recortar)
            # --- Mientras la longitud del cuadro sea mayor al ancho de la columna, este se recorta --- #
            while len(cuadro_a_recortar) > ancho[columna]:
                cuadro.append(cuadro_a_recortar[0:after])
                cuadro_a_recortar = cuadro_a_recortar[after:]
            # --- Si el contenido de cuadro a recortar es menor al ancho de la columna
            #     se rellena el faltante de espacios en blanco --- #
            if len(cuadro_a_recortar) < ancho[columna]:
                cuadro.append(cuadro_a_recortar + ' ' * (ancho[columna] - len(cuadro_a_recortar)))
            # --- Se recorta el cuadro generado segun el max_y_cuadro_threshold (alto maximo) --- #
            if len(cuadro) > max_y_cuadro_threshold:
                cuadro = cuadro[0:max_y_cuadro_threshold]

            # --- Se inserta cada cuadro en la tupla que se esta generando --- #
            cuadros_a_insertar.append(cuadro)

        # --- Se chequea el espacio maximo para cada cuadro --- #
        maximo = 0
        for cuadro in cuadros_a_insertar:
            if len(cuadro) > maximo:
                maximo = len(cuadro)
        # --- Se rellena de lineas en blanco el faltante a y_maximos --- #
        for columna in range(len(cuadros_a_insertar)):
            # Si la longitud del cuadro es menor al maximo(cuadro).
            while len(cuadros_a_insertar[columna]) < maximo:
                cuadros_a_insertar[columna].append(' ' * ancho[columna])

        # --- Se inserta cada tupla de cuadros en linea_cuadros. --- #
        linea_cuadros.append(cuadros_a_insertar)

    # --- Se retorna la lista linea_cuadros --- #
    return linea_cuadros


def asign_ancho_columnas(show_ancho_thresholding = 5, maximos = None, screen_x = None, ordered_lista_tipo_datos = None, cadena_prioridades = None, len_separador = 1, orden = None):
    # Variable en la cual se guardara el ancho para cada columna.
    anchos = []

    # Chequea si se proveen datos sobre el tipo de datos sobre la salida de la base de datos.
    # Estos deberian ser generados en check_lista_tipo_datos_integrity
    # Sin tipo, los anchos se asignan por igual basandose en la longitud de la pantalla.
    if ordered_lista_tipo_datos == None:
        # Se emite un error alertando de la falta de este dato, y se frena la ejecucion de asign_ancho_columnas.
        errores.append('Render > asign_ancho_columnas: ordered_lista_tipo_datos es None.')
        return anchos

    # Chequea si cadena_prioridades es None, si es asi, intenta detectarla.
    if cadena_prioridades == None:
        cadena_prioridades = check_cadena_prioridades(ordered_lista_tipo_datos)

    # Si screen_x es None, asigna 80, una medida muy comun, y emite un error.
    if screen_x == None or type(screen_x) != int:
        screen_x = 80
        errores.append('Render > asign_ancho_columnas: No se proveyo screen_x')

    # --- Estando ordered_lista_tipo_datos presente: --- #
    # Se chequea si se proveyeron datos sobre los maximos, estos deberian ser generados en check_maximos.
    if maximos == None:
        errores.append('Render > asign_ancho_columnas: No se proveyo maximos.')
        # Si no se provee este dato, se asignara el mismo ancho para todas las columnas.
        ancho = (screen_x - len_separador * (len(ordered_lista_tipo_datos) + 1)) / len(ordered_lista_tipo_datos)
        for columna in range(len(ordered_lista_tipo_datos)):
            anchos.append(ancho)
        return anchos

    # Obtiene el ancho medio de cada columna en base a espacio_restante.
    def get_ancho_medio():
        return int(espacio_restante / cantidad_columnas)

    need_rebuild = True
    while need_rebuild:
        # --- Estando ordered_lista_tipo_datos y maximos presente: --- #
        # Se desprovee a screen_x de los separadores, para obtener un dato claro sobre el espacio necesario.
        ancho_pantalla = screen_x - len_separador * (len(ordered_lista_tipo_datos) + 1)
        # Espacio que queda vacio en pantalla, inicialmente es toda la pantalla, osea, ancho_pantalla.
        espacio_restante = ancho_pantalla
        cantidad_columnas = len(ordered_lista_tipo_datos)

        anchos = []
        # Se genera una cadena de anchos rellena de ceros.
        for columna in range(cantidad_columnas):
            anchos.append('0')

        # Para cada columna de la tabla se define el ancho de la columna.
        for columna in cadena_prioridades:
            # Se convierte columna a int, ya que en cadena_prioridades es string.
            columna = int(columna)
            # Se obtiene el ancho medio del espacio de las columnas disponibles
            ancho_medio = get_ancho_medio()

            # Si el contenido de la columna es menor al ancho medio se asigna ese valor.
            if maximos[columna] < ancho_medio:
                anchos[columna] = maximos[columna]
            # Si es mayor el ancho pasa a ser el ancho medio
            else:
                anchos[columna] = ancho_medio

            # Se recalcula espacio_restante.
            espacio_restante -= int(anchos[columna])
            cantidad_columnas -= 1

        need_rebuild = False
        # Se revisan los anchos, en busqueda de elementos menores a show_ancho_thresholding.
        para_suprimir = ''
        for columna in range(len(anchos)):
            if anchos[columna] < show_ancho_thresholding:
                # or anchos[columna] < 0, se usa para evitar errores en pantallas en extremo finas.
                if ordered_lista_tipo_datos[columna] not in ['id', 'value', 'name'] or anchos[columna] < 0:
                    para_suprimir += str(columna)
                    need_rebuild = True

        # Si se detecto la necesidad de reconstruccion.
        if need_rebuild:
            # --- Se regenera la variable orden --- #
            # Si el orden es None, se genera un orden basado en ordered_lista_tipo_datos, del tipo 012..N
            if orden == None:
                orden = ''
                for elemento in range(len(ordered_lista_tipo_datos)):
                    orden += str(elemento)

            # Se suprimen los elementos a suprimir en el nuevo orden.
            new_orden = ''
            for x in range(len(orden)):
                if orden[x] not in para_suprimir:
                    new_orden += orden[x]

            # --- Se analizan nuevamente parametros en la tabla --- #
            ordered_lista_tipo_datos = reordenar_lista_tipo_datos(ordered_lista_tipo_datos, new_orden)
            cadena_prioridades = check_cadena_prioridades(ordered_lista_tipo_datos, None, True)

    return ordered_lista_tipo_datos, cadena_prioridades, anchos


def check_cadena_prioridades(ordered_lista_tipo_datos = None, cadena_prioridades = None, internal = False):
    # Esta funcion se encarga de chequear la integridad de las prioridades ingresadas.
    # En caso de ser deficientes (o ausentes), intenta reconstruirlas.
    if ordered_lista_tipo_datos == None:
        return 'Render: check_cadena_prioridades: No se proveyo ordered_lista_tipo_datos.'

    ##############################
    #   CHEQUEOS DE INTEGRIDAD   #
    ##############################
    # Estado que permite saber si se necesita o no reconstruccion.
    reconstruir = False

    # Si cadena_prioridades es None.
    if cadena_prioridades == None:
        reconstruir = True
        # internal es usada por las demas funciones para generar prioridades en modo silencioso.
        if internal == False:
            errores.append('Render > check_cadena_prioridades: cadena_prioridades no fue especificada.')
    else:
        # Longitud de cadena_prioridades.
        len_cadena_prioridades = len(cadena_prioridades)

    # Longitud de lista_tipo datos.
    len_ordered_lista_tipo_datos = len(ordered_lista_tipo_datos)

    # Si el texto de cadena_prioridades es numerico:
    if widgets.check_isnumerico(cadena_prioridades):
        # En caso de que la lista de prioridades sea mayor a ordered_lista_tipo_datos, se envia a reconstrir la lista.
        if len_cadena_prioridades > len_ordered_lista_tipo_datos:
            errores.append('Render > check_cadena_prioridades: cadena_prioridades es muy larga.')
            reconstruir = True

        # En caso de ser menor, se reconstruye el faltante.
        if len_cadena_prioridades < len_ordered_lista_tipo_datos:
            errores.append('Render > check_cadena_prioridades: cadena_prioridades es muy corta.')
            for x in range(len_cadsena_prioridades, len_ordered_lista_tipo_datos):
                reconstruir = True

        # Se chequea la integridad de los elementos.
        for x in range(len_cadena_prioridades):
            errores.append('Render > check_cadena_prioridades: cadena_prioridades no es integra.')
            if int(cadena_prioridades[x]) > len_ordered_lista_tipo_datos or int(cadena_prioridades[x]) < 0:
                reconstruir = True

    # Si se necesita reconstruir
    if reconstruir:
        # Se inicializa una cadena_prioridades vacia.
        cadena_prioridades = ''

        # Se intenta identificar elementos Id y Value, a los que se les asigna maxima prioridad.
        for elemento in range(len_ordered_lista_tipo_datos):
            if ordered_lista_tipo_datos[elemento] in ['id', 'value']:
                cadena_prioridades += str(elemento)

        # Se intenta identificar elementos name, asignandole su prioridad.
        for elemento in range(len_ordered_lista_tipo_datos):
            if ordered_lista_tipo_datos[elemento] == 'name':
                cadena_prioridades += str(elemento)

        # Se intenta identificar elementos date, asignandole su prioridad.
        for elemento in range(len_ordered_lista_tipo_datos):
            if ordered_lista_tipo_datos[elemento] == 'date':
                cadena_prioridades += str(elemento)

        # Se intenta identificar elementos time, asignandole su prioridad.
        for elemento in range(len_ordered_lista_tipo_datos):
            if ordered_lista_tipo_datos[elemento] == 'time':
                cadena_prioridades += str(elemento)

        # Se intenta identificar elementos desc, asignandole su prioridad.
        for elemento in range(len_ordered_lista_tipo_datos):
            if ordered_lista_tipo_datos[elemento] == 'desc':
                cadena_prioridades += str(elemento)

        # Si hay elementos sin identificar en ordered_lista_tipo_datos, se rellena el faltante con prioridades minimas.
        if len(cadena_prioridades) < len_ordered_lista_tipo_datos:
            errores.append('Render > check_cadena_prioridades: ordered_lista_tipo_datos contiene elementos no identificables')
            for elemento in range(len_cadena_prioridades, len_ordered_lista_tipo_datos):
                cadena_prioridades += str(elemento)

    return cadena_prioridades


# Esta funcion reordena lista_tipo_datos en base al orden provisto.
def reordenar_lista_tipo_datos(lista_tipo_datos = None, orden = None):
    # Se chequea si se proveyeron datos.
    if lista_tipo_datos == None:
        return 'Render > reordenar_lista_tipo_datos: No se proveyeron datos.'

    # Si no se provee orden, o este no es list, se retorna lista_tipo_datos sin mas.
    if orden == None or type(orden) != list:
        return lista_tipo_datos
    else:
        ordered_lista_tipo_datos = []
        # Se genera la tupla reordenada.
        for elemento in orden:
            try:
                ordered_lista_tipo_datos.append(lista_tipo_datos[int(elemento)])
            except:
                errores.append('Render > reordenar_lista_tipo_datos: Error al intentar reordenar lista_tipo_datos.')
                return lista_tipo_datos

        # Si se pudo reordenar sin errores, retorna lista_tipo_datos ordenada.
        return ordered_lista_tipo_datos


# Esta funcion chequea la integridad de los datos.
def check_data_integrity(data = None):
    # Se chequea si se proveyeron datos.
    if data == None:
        return 'Render > check_data_integrity: No se proveyeron datos.'

    error = False
    # Se chequea que el dato enviado sea una lista.
    if type(data) != list:
        error = True
    else:
        if len(data) > 0:
            # Se chequea que, dentro de la lista, los elementos sean listas.
            for tupla in data:
                if type(tupla) != tuple:
                    error = True
                # Se chequea que los elementos de las tuplas no sean listas o bool.
                try:
                    for elemento in tupla:
                        if type(elemento) == list or type(elemento) == bool:
                            error = True
                except:
                    error = True

            if len(data) > 0:
                try:
                    longitud_primera_tupla = len(data[0])
                    for tupla in data:
                        if len(tupla) != longitud_primera_tupla:
                            error = True
                except:
                    error = True
        else:
            error = True

    if error == True:
        errores.append('--- Render > check_data_integrity: Dato invalido o no integro ---')
    return error


def check_lista_tipo_datos_integrity(analyze_threshold = 10, data = None, lista_tipo_datos = None):
    # Se chequea si se proveyeron datos.
    if data == None:
        return 'Render > check_lista_tipo_datos_integrity: No se proveyeron datos.'

    # Se emite un error si no se provee la lista de tipos de datos.
    if lista_tipo_datos == None:
        errores.append('Render > check_lista_tipo_datos_integrity: No se proveyo lista_tipo_datos.')

    # --- Lista de elementos que deben intentar ser detectados --- #
    to_rebuild = []

    # Se chequea si hay tuplas en los datos provistos.
    if len(data) > 0:
        # Si la entrada para lista_tipo_datos es invalida, se preparan datos para reconstruirla.
        if type(lista_tipo_datos) != list:
            lista_tipo_datos = []
            for x in range(len(data[0])):
                lista_tipo_datos.append(None)
                to_rebuild.append(x)

        # Si la lista de tipo de datos tiene mas elementos que columnas los datos, la lista se recorta.
        if len(lista_tipo_datos) > len(data[0]):
            lista_tipo_datos = lista_tipo_datos[0:len(data[0])]
            errores.append('Render > check_lista_tipo_datos_integrity: Fue necesario acortar lista_tipo_datos.')
        # Si es menor, se agrega None a lista_tipo_datos.
        elif len(lista_tipo_datos) < len(data[0]):
            errores.append('Render > check_lista_tipo_datos_integrity: lista_tipo_datos es muy corta.')
            for x in range(len(lista_tipo_datos),len(data[0])):
                lista_tipo_datos.append(None)

        contador = 0
        # --- Se chequea que los elementos de lista_tipo_datos pertenezcan a los tipos admitidos --- #
        for elemento in lista_tipo_datos:
            if not elemento in ['id', 'name', 'date', 'time', 'value', 'desc']:
                # Si no pertenecen, se envia a reconstruir lo necesario.
                to_rebuild.append(contador)
            contador += 1

        # --- Se chequean y establecen la cantidad de tuplas a analizar --- #
        if len(data) > analyze_threshold:
            analyze = analyze_threshold
        else:
            analyze = len(data)

        #####################################
        # --- Seccion de reconstruccion --- #
        #####################################
        # --- Se chequea si hay datos para reconstruir --- #
        if len(to_rebuild) > 0:
            # --- Se reconstruyen los elementos invalidos o faltantes de la lista --- #
            for x in to_rebuild:
                # --- Se analiza cada elemento de la columna, intentando determinar a que tipo pertenece --- #
                # lista_tipos almacena los tipos detectados.
                lista_tipos = []
                # --- Para cada elemento en el rango de tuplas a analizar --- #
                for tupla in range(analyze):
                    # data[tupla][x], es un elemento de la columna.
                    # --- Chequea si el elemento se corresponde con una hora --- #
                    if widgets.ishora_complete(str(data[tupla][x])):
                        tipo = 'time'
                    # --- Chequea si el elemento se corresponde con una fecha --- #
                    elif widgets.isfecha(str(data[tupla][x])):
                        tipo = 'date'
                    # --- Chequea si el elemento es numerico --- #
                    elif widgets.check_isnumerico(str(data[tupla][x])):
                        # Intenta identificar si el elemento es numerico o Id
                        try:
                            if int(data[tupla + 1][x]) - int(data[tupla][x]) == 1:
                                tipo = 'id'
                            else:
                                tipo = 'value'
                        except:
                            tipo = 'value'
                        if tupla != 0:
                            try:
                                if int(data[tupla][x]) - int(data[tupla - 1][x]) == 1:
                                    tipo = 'id'
                                else:
                                    tipo = 'value'
                            except:
                                pass
                    # --- Si no es numerico, se asume que es texto --- #
                    else:
                        if len(str(data[tupla][x])) > 15:
                            num_letras = 0
                            # Se cuenta el numero de letras en el elemento.
                            for letra in str(data[tupla][x]):
                                if letra in letras:
                                    num_letras += 1
                            # Se toma como name si tiene 90% de letras.
                            if (num_letras * 100 / len(str(data[tupla][x]))) > 90:
                                tipo = 'name'
                            else:
                                tipo = 'desc'
                        else:
                            tipo = 'name'

                    # Se añade el tipo a la lista_tipos generada
                    lista_tipos.append(tipo)

                # --- Se analizan los datos obtenidos (pertenecientes a una columna) --- #
                tipo_date = 0
                tipo_time = 0
                tipo_id = 0
                tipo_value = 0
                tipo_name = 0
                tipo_desc = 0
                for a in lista_tipos:
                    if a == 'date':
                        tipo_date += 1
                    elif a == 'time':
                        tipo_time += 1
                    elif a == 'id':
                        tipo_id += 1
                    elif a == 'value':
                        tipo_value += 1
                    elif a == 'name':
                        tipo_name += 1
                    elif a == 'desc':
                        tipo_desc += 1
                # --- Se procesan los datos del analisis y se integra a la lista de prioridades --- #
                # Se obtienen los porcentajes en los cuales cada tipo esta presente dentro del analyze.
                tipo_date *= 100 / analyze
                tipo_time *= 100 / analyze
                tipo_id *= 100 / analyze
                tipo_value *= 100 / analyze
                tipo_name *= 100 / analyze
                tipo_desc *= 100 / analyze
                # --- Se deduce que resultado es a partir de la correspondencia de los resultados con el thresholding.
                if tipo_date >= 70:
                    tipo = 'date'
                elif tipo_time >= 70:
                    tipo = 'time'
                elif tipo_id >= 50:
                    tipo = 'id'
                elif tipo_value == 100:
                    tipo = 'value'
                elif tipo_name >= 60:
                    tipo = 'name'
                elif tipo_desc >= 60:
                    tipo = 'desc'
                else:
                    tipo = 'desc'

                # Se asigna el tipo averiguado a la lista_tipo_datos
                lista_tipo_datos[x] = tipo

        if len(to_rebuild) > 0:
            errores.append('Render > check_lista_tipo_datos_integrity: Fue necesario reconstruir lista_tipo_datos.')

        # Se retorna la lista de tipos de datos.
        return lista_tipo_datos


# Esta funcion reordena columnas en base a un recordset.
def reordenar_datos(data = None, orden = None):
    # Se chequea si se proveyeron datos.
    if data == None:
        return 'Render > reordenar_datos: No se proveyeron datos.'
    else:
        # Chequea si la entrada a reordenar_datos es la correcta
        if orden == None or type(orden) != list:
            ordered_data = data
        else:
            ordered_data = []
            for tupla in data:
                new_tupla = []
                # Se genera la tupla reordenada.
                for elemento in orden:
                    try:
                        new_tupla.append(tupla[int(elemento)])
                    except:
                        errores.append('Render > reordenar_datos: Error al intentar reordenar los datos.')
                        return data
                # Se añade la tupla generada al nuevo recordset.
                ordered_data.append(new_tupla)
        return ordered_data


def check_separador(separador = None, screen_x = 80):
    if separador == None or type(separador) != str:
        return ' '
    elif len(separador) > screen_x:
        errores.append('Render > check_separador: El separador provisto es invalido')
        return ' '
    else:
        return separador


def check_orden(data = None, orden = None):
    if data == None:
        errores.append('Render > check_orden: No se proveyo data.')
        return []

    # --- Se chequea la validez del orden provisto en base a sus propiedades --- #
    if orden == None or type(orden) != list:
        errores.append('Render > check_orden: El orden es invalido o no fue provisto.')
        if len(data) > 0:
            orden = []
            for x in range(len(data[0])):
                orden.append(x)
            return orden
        else:
            return []

    # --- Se analiza si los elementos del orden son validos en referencia a los datos --- #
    # Lista de elementos a remover
    to_remove = []
    if len(data) > 0:
        # Para cada elemento en len(orden)
        for x in range(len(orden)):
            # Si el orden es numerico
            if widgets.check_isnumerico(orden[x]):
                # Si el numero que contiene orden[x] es mayor al numero de columnas del recordset se remueve
                if orden[x] >= len(data[0]):
                    to_remove.append(orden[x])
            # Si no lo es, se remueve
            else:
                to_remove.append(orden[x])
    else:
        return []

    for x in to_remove:
        orden.remove(x)

    return orden


# Chequea la longitud maxima para mostrar cada campo, asigna la longitud a maximo[x]
def check_maximos(ordered_data = None):
    # Se chequea si se proveyeron datos.
    if ordered_data == None:
        return 'Render > check_maximos: No se proveyeron datos ordenados.'

    if len(ordered_data) > 0:
        maximo = []
        # Rellena de ceros los valores maximos para cada elemento
        for columna in ordered_data[0]:
            maximo.append(0)
        # Mide los elementos de la tabla y asigna maximos para cada elemento.
        for tupla in range(len(ordered_data)):
            for elemento in range(len(ordered_data[0])):
                if len(str(ordered_data[tupla][elemento])) > maximo[elemento]:
                    maximo[elemento] = len(str(ordered_data[tupla][elemento]))
        return maximo
    else:
        errores.append('Render > check_maximos: Error al intentar chequear el maximo.')
