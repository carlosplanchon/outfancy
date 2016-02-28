#!/usr/bin/python3
# -*- coding: utf-8 -*-

from . import widgets

letras = 'abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
minus_letters = 'abcdefghijklmnñopqrstuvwxyz'

# Start check.
widgets.start_check()

class Chart:
    """Chart allow to render a chart with nice format, the data input have to acomplish the format [(1, 'foo'), (2, 'bar')]"""
    def __init__(self):
        '''Rendering parameters.'''
        # Check_data specify if the input data have to be checked or not.
        self.check_data = True
        # Check_dimensiones especifica si debe chequearse o no el tamaño de los datos del recordset. 
        self.check_dimensiones = False
        # Corrector = Indica el valor de correcion a aplicar en el eje x (margen en blanco a la derecha. de la pantalla).
        self.corrector = -2
        # Alto maximo que puede tener una tupla en pantalla.
        self.max_y_cuadro_threshold = 20
        # Threshold de analisis al reconstruir datos de screen.lista_tipo_datos.
        self.analyze_threshold = 10
        # El ancho minimo que puede tener una columna antes de que se deje de mostrar.
        self.show_width_threshold = 5

        '''Dimensions'''
        # La cantidad maxima de filas que puede tener una tabla (-1 = ilimitadas).
        self.cantidad_maxima_filas = -1

        '''Options'''
        # Con esta opcion los errores se muestran en pantalla luego de la impresion.
        self.show_errores = False
        # Se especifica si se registran o no errores en el log del programa.
        self.log_errores = False
        # Se especifica si deben mostrarse o no las etiquetas sobre la tabla.
        self.show_etiquetas = True


    def set_check_data(self, x=True):
        self.check_data = x

    def set_check_dimensiones(self, x=True):
        self.check_dimensiones = x

    def set_corrector(self, x=-2):
        self.corrector = x

    def set_max_y_cuadro_threshold(self, x=20):
        self.max_y_cuadro_threshold = x

    def set_analyze_threshold(self, x=10):
        self.analyze_threshold = x

    def set_show_ancho_threshold(self, x=True):
        self.show_width_threshold = x

    def set_show_errores(self, x=True):
        self.show_errores = x

    def set_log_errores(self, x=True):
        self.log_errores = x

    def set_show_etiquetas(self, x=True):
        self.show_etiquetas = x

    def set_cantidad_maxima_filas(self, x=-1):
        self.cantidad_maxima_filas = x


    def show_check_data(self):
        print(self.check_data)

    def show_check_dimensiones(self):
        print(self.check_dimensiones)

    def show_corrector(self):
        print(self.corrector)

    def show_max_y_cuadro_threshold(self):
        print(self.max_y_cuadro_threshold)

    def show_analyze_threshold(self):
        print(self.analyze_threshold)

    def show_show_ancho_threshold(self):
        print(self.show_width_threshold)

    def show_show_errores(self):
        print(self.show_errores)

    def show_log_errores(self):
        print(self.log_errores)

    def show_show_etiquetas(self):
        print(self.show_etiquetas)

    def show_cantidad_maxima_filas(self):
        print(self.cantidad_maxima_filas)


    def render(self, data=None, separador=None, lista_etiquetas=None, orden=None, lista_tipo_datos=None, lista_prioridades=None, anchos=None):
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
        lista_prioridades: Permite modificar la prioridad que se le asigna a cada columna, si no se especifica
        el programa asignara prioridades en base a lista_tipo_datos.
        Si el espacio para mostrar las columnas no es suficiente, el programa podra suprimir columnas
        (iniciando por las de baja prioridad).
        anchos: Permite especificar anchos para las columnas.
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
            if self.check_data_integrity(data):
                return '--- Recordset > Render > check_data_integrity: Dato invalido o no integro ---'

        # --- Si en configuracion se especifica, se chequean las dimensiones de los datos --- #
        if self.check_dimensiones:
            if self.check_dimensiones_correctas(data):
                return '--- Recordset > Render: El dato tiene mas lineas que las permitidas. --- '

        ##############################
        # --- AREA DE PRE-RENDER --- #
        ##############################
        # --- Se analizan las dimensiones de la pantalla --- #
        screen_x, screen_y = widgets.measure_screen()
        # --- Se aplica valor de correccion a screen_x --- #
        screen_x += self.corrector
        # --- Se chequea el separador --- #
        separador = self.check_separador(separador, screen_x)
        # --- Se chequea la validez del orden provisto --- #
        orden = self.check_orden(data, orden)
        # --- Se reordenan los datos y las etiquetas --- #
        ordered_data = self.reordenar_datos(data, orden)
        # --- Chequea la longitud maxima para mostrar cada campo de ordered_data --- #
        maximo = self.check_maximos(ordered_data)
        # --- Se chequea la integridad de la lista de tipos de datos --- #
        lista_tipo_datos = self.check_lista_tipo_datos_integrity(lista_etiquetas, lista_prioridades, data, lista_tipo_datos)
        # --- Se reordena lista_tipo_datos --- #
        ordered_lista_tipo_datos = self.reordenar_lista_tipo_datos(lista_tipo_datos, orden)
        # --- Se chequea la integridad de lista_prioridades, si no existe o es defectuosa, se intenta reconstruir --- #
        lista_prioridades = self.check_lista_prioridades(ordered_lista_tipo_datos, lista_prioridades)
        ##########################
        # --- AREA DE RENDER --- #
        ##########################
        # --- Asigna el ancho para mostrar las columnas, si este no es provisto, intenta deducirlo --- #
        anchos, orden = self.asign_ancho_columnas(anchos, lista_prioridades, maximo, screen_x, len(separador), len(orden))
        # --- Por 2da vez: Se reordena lista_tipo_datos --- #
        ordered_lista_tipo_datos = self.reordenar_lista_tipo_datos(lista_tipo_datos, orden)
        # --- Por 2da vez: Se reordenan los datos --- #
        ordered_data = self.reordenar_datos(data, orden)        
        # --- Genera las casillas que contienen los datos --- #
        linea_cuadros = self.generar_cuadros_pantalla(ordered_data, anchos, maximo, screen_y)
        # --- Genera el area de la pantalla que contiene el pre_render del recordset --- #
        pantalla = self.generar_pantalla(linea_cuadros, separador)
        # --- Chequea la lista de etiquetas --- #
        lista_etiquetas = self.check_lista_etiquetas(lista_etiquetas, lista_tipo_datos, anchos, orden, separador)
        ###############################
        # --- AREA DE POST-RENDER --- #
        ###############################
        # --- Lleva a cabo el post_render, uniendo el pre_render del recordset con los demas datos --- #
        return self.post_render(pantalla, lista_etiquetas, len(separador))


    def test(self):
        # Funcion de demostracion.
        recordset = [(1, 'Feisbuk', '18-10-2015', '21:57:17', '18-10-2015', '21:57:17', 1234, 'Red social bla bla bla utilizada por gente bla bla.'), (2, 'Gugle', '18-10-2015', '21:57:44', '18-10-2015', '21:57:44', 12323, 'Motor de busqueda que categoriza resultados por la cantidad de links bla bla bla.'), (3, 'Opera', '18-10-2015', '21:58:39', '18-10-2015', '21:58:39', 4324, 'Navegador de internerd, también es una disciplina musical, que, valga la redundancia, requiere de una brutal disciplina por parte de los interpretes.'), (4, 'Audi', '18-10-2015', '21:59:51', '18-10-2015', '21:59:51', 0, 'OOOO <-- Fabricante alemán de vehiculos de alta gama.'), (5, 'The Simpsons', '18-10-2015', '22:0:44', '18-10-2015', '22:0:44', 0, 'Una sitcom que lleva veintipico de temporadas, si no la viste, se puede presumir que vivís bajo una piedra.'), (6, 'BMW', '18-10-2015', '22:1:18', '18-10-2015', '22:1:18', 98765, 'Fabricante alemán de autos de lujo.'), (7, 'Yahoo', '18-10-2015', '22:1:56', '18-10-2015', '22:1:56', 53430, 'Expresión de alegría, o compañía gringolandesa.'), (8, 'Coca Cola', '18-10-2015', '22:3:19', '18-10-2015', '22:3:19', 200, 'Compañía que fabrica bebidas, y que no nos paga por ponerla en py-test :c.'), (9, 'Pepsi', '18-10-2015', '22:3:40', '18-10-2015', '22:3:40', 340, 'Competidora de la anterior compañía mencionada, y que tampoco nos paga :c.'), (10, 'GitHub', '18-10-2015', '22:4:42', '18-10-2015', '22:4:42', 563423, 'Plataforma de gestión de co0o0o0ó0digo.'), (11, 'Johnny Walker', '18-10-2015', '22:5:34', '18-10-2015', '22:5:34', 4252, 'Whisky escocés.'), (12, 'Mercury', '18-10-2015', '22:5:51', '18-10-2015', '22:5:51', 23423, 'Fabricante de motores fuera de borda.'), (13, 'Rolls Royce', '18-10-2015', '22:6:7', '18-10-2015', '22:6:7', 75832, 'Fabricante de motores para aviones, y autos de alta gama.')]
        input('--- Presione ENTER para ver el recordset tal cual es ---')
        print(recordset)
        input('--- Ahora presione ENTER para ver el recordset renderizado por Outfancy ---')
        print(self.render(recordset))


    # Esta funcion chequea la integridad de los datos.
    def check_dimensiones_correctas(self, data=None):
        # Se chequea si se proveyeron datos.
        if data == None:
            return 'Recordset > Render > check_dimensiones: No se proveyeron datos.'

        # Se chequea que los datos no tengan mas filas que las permitidas.
        if len(data) > self.cantidad_maxima_filas and self.cantidad_maxima_filas > -1:
            return True
        else:
            return False

    # Esta funcion chequea la integridad de los datos.
    def check_data_integrity(self, data=None):
        # Se chequea si se proveyeron datos.
        if data == None:
            return 'Recordset > Render > check_data_integrity: No se proveyeron datos.'

        error = False
        # Se chequea que el dato enviado sea una lista.
        if not isinstance(data, list):
            error = True
        else:
            if len(data) > 0:
                # Se chequea que, dentro de la lista, los elementos sean listas.
                for tupla in data:
                    if not isinstance(tupla, tuple):
                        error = True
                    # Se chequea que los elementos de las tuplas no sean listas o bool.
                    try:
                        for elemento in tupla:
                            if isinstance(elemento, (list, bool)):
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
            errores.append('--- Recordset > Render > check_data_integrity: Dato invalido o no integro ---')
        return error


    def check_separador(self, separador=None, screen_x=80):
        if not isinstance(separador, str):
            return ' '
        elif len(separador) > screen_x:
            errores.append('Recordset > Render > check_separador: El separador provisto es invalido')
            return ' '
        else:
            return separador


    def check_orden(self, data=None, orden=None):
        if data == None:
            errores.append('Recordset > Render > check_orden: No se proveyo data.')
            return []

        # --- Se chequea la validez del orden provisto en base a sus propiedades --- #
        if not isinstance(orden, list):
            errores.append('Recordset > Render > check_orden: El orden es invalido o no fue provisto.')
            if len(data) > 0:
                orden = []
                for x in range(len(data[0])):
                    orden.append(x)
                return orden
            else:
                return []

        # --- Se analiza si los elementos del orden son validos en referencia a los datos --- #
        # Lista de elementos a remover.
        to_remove = []
        if len(data) > 0:
            # Para cada elemento en len(orden)
            for x in range(len(orden)):
                # Si el orden es numerico
                if widgets.check_isnumeric(orden[x]):
                    # Si el numero que contiene orden[x] es mayor al numero de columnas del recordset o menor a 0 se remueve.
                    if orden[x] >= len(data[0]) or orden[x] < -1:
                        to_remove.append(orden[x])
                # Si el orden no es numerico, se remueve.
                else:
                    to_remove.append(orden[x])
        else:
            return []

        for x in to_remove:
            orden.pop(x)

        return orden


    # Esta funcion reordena columnas en base a un recordset.
    def reordenar_datos(self, data=None, orden=None):
        # Se chequea si se proveyeron datos.
        if data == None:
            return 'Recordset > Render > reordenar_datos: No se proveyeron datos.'
        else:
            # Chequea si la entrada a reordenar_datos es la correcta
            if not isinstance(orden, list):
                ordered_data = data
            else:
                ordered_data = []
                for tupla in data:
                    new_tupla = []
                    # Se genera la tupla reordenada.
                    for elemento in orden:
                        try:
                            new_tupla.append(tupla[elemento])
                        except:
                            errores.append('Recordset > Render > reordenar_datos: Error al intentar reordenar los datos.')
                            return data
                    # Se añade la tupla generada al nuevo recordset.
                    ordered_data.append(new_tupla)
            return ordered_data


    # Chequea la longitud maxima para mostrar cada campo, asigna la longitud a maximo[x].
    def check_maximos(self, ordered_data=None):
        # Se chequea si se proveyeron datos.
        if ordered_data == None:
            return 'Recordset > Render > check_maximos: No se proveyeron datos ordenados.'

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
            errores.append('Recordset > Render > check_maximos: Error al intentar chequear el maximo.')


    def check_lista_tipo_datos_integrity(self, lista_etiquetas=False, lista_prioridades=None, data=None, lista_tipo_datos=None):
        # Si lista_etiquetas y lista_prioridades son False, lista_tipo_datos no se chequea por ser irrelevante en este caso de uso.
        if lista_etiquetas == False and lista_prioridades == False:
            return False

        # Se chequea si se proveyeron datos.
        if data == None:
            return 'Recordset > Render > check_lista_tipo_datos_integrity: No se proveyeron datos.'

        # Se emite un error si no se provee la lista de tipos de datos.
        if lista_tipo_datos == None:
            errores.append('Recordset > Render > check_lista_tipo_datos_integrity: No se proveyo lista_tipo_datos.')

        # --- Lista de elementos que deben intentar ser detectados --- #
        to_rebuild = []

        # Se chequea si hay tuplas en los datos provistos.
        if len(data) > 0:
            # Si la entrada para lista_tipo_datos es invalida, se preparan datos para reconstruirla.
            if not isinstance(lista_tipo_datos, list):
                lista_tipo_datos = []
                for x in range(len(data[0])):
                    lista_tipo_datos.append(None)
                    to_rebuild.append(x)

            # Si la lista de tipo de datos tiene mas elementos que columnas los datos, la lista se recorta.
            if len(lista_tipo_datos) > len(data[0]):
                lista_tipo_datos = lista_tipo_datos[0:len(data[0])]
                errores.append('Recordset > Render > check_lista_tipo_datos_integrity: Se acorto lista_tipo_datos.')
            # Si es menor, se agrega None a lista_tipo_datos.
            elif len(lista_tipo_datos) < len(data[0]):
                errores.append('Recordset > Render > check_lista_tipo_datos_integrity: lista_tipo_datos es muy corta.')
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
            if len(data) > self.analyze_threshold:
                analyze = self.analyze_threshold
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
                        if widgets.is_complete_hour(str(data[tupla][x])):
                            tipo = 'time'
                        # --- Chequea si el elemento se corresponde con una fecha --- #
                        elif widgets.is_date(str(data[tupla][x])):
                            tipo = 'date'
                        # --- Chequea si el elemento es numerico --- #
                        elif widgets.check_isnumeric(str(data[tupla][x])):
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
                errores.append('Recordset > Render > check_lista_tipo_datos_integrity: Fue necesario reconstruir lista_tipo_datos.')

            # Se retorna la lista de tipos de datos.
            return lista_tipo_datos


    # Esta funcion reordena lista_tipo_datos en base al orden provisto.
    def reordenar_lista_tipo_datos(self, lista_tipo_datos=None, orden=None):
        # Se chequea si se proveyeron datos.
        if lista_tipo_datos == None:
            raise Exception('Recordset > Render > reordenar_lista_tipo_datos: No se proveyo lista_tipo_datos.')

        # Si no se provee orden, o este no es list, se retorna lista_tipo_datos sin mas.
        if not isinstance(orden, list):
            errores.append('Recordset > Render > reordenar_lista_tipo_datos: No se proveyo orden o este no es valido.')
            return lista_tipo_datos
        else:
            ordered_lista_tipo_datos = []
            # Se genera la tupla reordenada.
            for elemento in orden:
                try:
                    ordered_lista_tipo_datos.append(lista_tipo_datos[elemento])
                except:
                    errores.append('Recordset > Render > reordenar_lista_tipo_datos: Error al intentar reordenar lista_tipo_datos.')
                    return lista_tipo_datos

            # Si se pudo reordenar sin errores, retorna lista_tipo_datos ordenada.
            return ordered_lista_tipo_datos


    def check_lista_prioridades(self, ordered_lista_tipo_datos=None, lista_prioridades=None, internal=False):
        # Esta funcion se encarga de chequear la integridad de las prioridades ingresadas.
        # En caso de ser deficientes (o ausentes), intenta reconstruirlas.

        # Si lista_etiquetas es False, se retorna, ya que este valor tiene validez en otras partes del programa.
        if lista_prioridades == False:
            return lista_prioridades

        if ordered_lista_tipo_datos == None:
            raise Exception('Render: check_lista_prioridades: No se proveyo ordered_lista_tipo_datos.')

        # Longitud de lista_tipo datos.
        len_ordered_lista_tipo_datos = len(ordered_lista_tipo_datos)

        ##############################
        #   CHEQUEOS DE INTEGRIDAD   #
        ##############################
        # Estado que permite saber si se necesita o no reconstruccion.
        reconstruir = False

        # Si lista_prioridades es None.
        if not isinstance(lista_prioridades, list):
            reconstruir = True
            # internal es usada por las demas funciones para generar prioridades en modo silencioso.
            if internal == False:
                errores.append('Recordset > Render > check_lista_prioridades: No se proveyo lista_prioridades o esta es invalida.')
        else:
            # Longitud de lista_prioridades.
            len_lista_prioridades = len(lista_prioridades)

            # Si lista_prioridades no es None
            if lista_prioridades != None:
                # Si un elemento de lista_prioridades no es numerico, reconstruir es True.
                for x in lista_prioridades:
                    if not isinstance(x, int):
                        reconstruir = True

            # En caso de que len_lista de prioridades sea mayor a ordered_lista_tipo_datos, reconstruir = True.
            if len_lista_prioridades > len_ordered_lista_tipo_datos:
                errores.append('Recordset > Render > check_lista_prioridades: lista_prioridades es muy larga.')
                reconstruir = True

            # En caso de que len_lista de prioridades sea mayor a ordered_lista_tipo_datos, reconstruir = True.
            if len_lista_prioridades < len_ordered_lista_tipo_datos:
                errores.append('Recordset > Render > check_lista_prioridades: lista_prioridades es muy corta.')
                reconstruir = True

            # Se chequea la integridad de los elementos.
            for x in lista_prioridades:
                if x >= len_ordered_lista_tipo_datos or x < 0:
                    reconstruir = True
                if reconstruir:
                    errores.append('Recordset > Render > check_lista_prioridades: lista_prioridades no es integra.')

        # Si se necesita reconstruir
        if reconstruir:

            # Se inicializa una lista_prioridades vacia.
            lista_prioridades = []

            # Se intenta identificar elementos Id y Value, a los que se les asigna maxima prioridad.
            for elemento in range(len_ordered_lista_tipo_datos):
                if ordered_lista_tipo_datos[elemento] in ['id', 'value']:
                    lista_prioridades.append(elemento)

            # Se intenta identificar elementos name, asignandole su prioridad.
            for elemento in range(len_ordered_lista_tipo_datos):
                if ordered_lista_tipo_datos[elemento] == 'name':
                    lista_prioridades.append(elemento)

            # Se intenta identificar elementos date, asignandole su prioridad.
            for elemento in range(len_ordered_lista_tipo_datos):
                if ordered_lista_tipo_datos[elemento] == 'date':
                    lista_prioridades.append(elemento)

            # Se intenta identificar elementos time, asignandole su prioridad.
            for elemento in range(len_ordered_lista_tipo_datos):
                if ordered_lista_tipo_datos[elemento] == 'time':
                    lista_prioridades.append(elemento)

            # Se intenta identificar elementos desc, asignandole su prioridad.
            for elemento in range(len_ordered_lista_tipo_datos):
                if ordered_lista_tipo_datos[elemento] == 'desc':
                    lista_prioridades.append(elemento)

            # Si hay elementos sin identificar en ordered_lista_tipo_datos, se rellena el faltante con prioridades minimas.
            if len(lista_prioridades) < len_ordered_lista_tipo_datos:
                errores.append('Recordset > Render > check_lista_prioridades: ordered_lista_tipo_datos contiene elementos no identificables')
                for elemento in range(len(lista_prioridades), len_ordered_lista_tipo_datos):
                    lista_prioridades.append(elemento)

        return lista_prioridades


    def asign_ancho_columnas(self, anchos=None, ordered_lista_prioridades=False, maximos=None, screen_x=None, len_separador=None, len_order=None):
        # Si len_separador no es provista o es menor a 0 se restaura a 1 y se emite un error.
        if not isinstance(len_separador, int) or len_separador < 0:
            len_separador = 1
            errores.append('Recordset > Render > asign_ancho_columnas: No se proveyo len_separador o este es invalido.')

        # Si no se provee len_order ni ordered_lista_prioridades.
        if len_order == None and maximos == None and not isinstance(ordered_lista_prioridades, list):
            raise Exception('Recordset > Render > asign_ancho_columnas: No se proveyo ordered_lista_prioridades ni len_order ni maximos.')

        # Si len_order no es provisto o es menor a 0 se restaura a 1 y se emite un error.
        if not isinstance(len_order, int) or len_order < 0:
            errores.append('Recordset > Render > asign_ancho_columnas: No se proveyo len_order o este es invalido.')

        # Se intenta reconstruir len_order a partir de ordered_lista_prioridades.
        if len_order == None and isinstance(ordered_lista_prioridades, list):
            len_order = len(ordered_lista_prioridades)

        # Se intenta reconstruir len_order a partir de maximos.
        if len_order == None and isinstance(maximos, list):
            len_order = len(maximos)

        # Obtiene el ancho medio de cada columna en base a remaining_space.
        def get_ancho_medio(remaining_space, len_order):
            if len_order == 0:
                return 0
            else:
                return int(remaining_space / len_order)

        def get_espacio_pantalla():
            # Se desprovee a screen_x de los separadores, para obtener un dato claro sobre el espacio existente.
            return screen_x - len_separador * len_order     

        # Se crea el orden que toma como base asign_ancho_columnas a la hora de comunicar los cambios hechos en las variables generales.
        orden = []
        for x in range(len_order):
            orden.append(x)

        # Si anchos es provisto, los chequea, y, en caso de ser validos lo retorna.
        a_reconstruir = False
        longitud_total_elementos = 0
        # Si el elemento es una lista.
        if isinstance(anchos, list):
            # Se chequea que cada elemento sea numerico, y que su suma no sea mayor al espacio disponible.
            for elemento in anchos:
                if isinstance(elemento, int):
                    if elemento > 0:
                        longitud_total_elementos += elemento
                    else:
                        a_reconstruir = True
                else:
                    a_reconstruir = True
        else:
            a_reconstruir = True

        # Si el total de los anchos es mayor al espacio de la pantalla, se envia este a reconstruir.
        if longitud_total_elementos > get_espacio_pantalla():
            a_reconstruir = True

        # Si el chequeo demuestra que todo esta en orden, se retornan los anchos.
        if not a_reconstruir:
            return anchos, orden

        # Si screen_x es None o es menor a 1, asigna 80, una medida muy comun, y emite un error.
        if not isinstance(screen_x, int) or screen_x < 1:
            screen_x = 80
            errores.append('Recordset > Render > asign_ancho_columnas: No se proveyo screen_x o este es invalido.')

        # Si show_ancho_threshold no es provisto o es menor a 1, lo asigna a 5 y emite un error.
        if not isinstance(self.show_width_threshold, int) or self.show_width_threshold < 1:
            self.show_width_threshold = 5
            errores.append('Recordset > Render > asign_ancho_columnas: No se proveyo show_ancho_threshold o este es invalido.')

        # Si ordered_lista_prioridades == False, se asigna el mismo ancho a todas las columnas en base a len(orden).
        # Si maximos no fue provisto o es invalido se emite un error y se reconstruye.
        if not isinstance(maximos, list) or ordered_lista_prioridades == False or anchos == False:
            errores.append('Recordset > Render > asign_ancho_columnas: No se proveyo maximos o este es invalido.')
            maximos = []

            checking = True
            while checking:
                if len_order > 0:
                    ancho_medio = get_ancho_medio(get_espacio_pantalla(), len_order)
                    # Si el ancho_medio es menor o igual a 0.
                    if ancho_medio <= 0:
                        # Se elimina el elemento de menor prioridad.
                        ordered_lista_prioridades = widgets.compress_lista(ordered_lista_prioridades[0:len_order - 1])
                        len_order -= 1
                    else:
                        checking = False
                else:
                    ancho_medio = 0
                    checking = False

            # Los maximos para cada columna son iguales al ancho_medio obtenido en funcion del ancho de la pantalla.
            for x in range(len_order):
                maximos.append(ancho_medio)

        # Se chequea lista_prioridades.
        if isinstance(ordered_lista_prioridades, bool) or ordered_lista_prioridades == None:
            ordered_lista_prioridades = []
            for x in range(len_order):
                ordered_lista_prioridades.append(x)       

        no_finalizado = True
        while no_finalizado:
            # Lista vacia que contendra los anchos.
            anchos = []
            # Lista para registrar maximos menores a show_ancho_thresholding. 
            maxima_less_than_show_width_threshold = []

            # remaining_space se inicializa igual al espacio disponible en pantalla, a medida que se vaya usando se acortara.
            remaining_space = get_espacio_pantalla()

            for x in range(len_order):
                anchos.append(0)

            # Para cada elemento de lista prioridades.
            # Notar que se asigna espacio iniciando por la mayor prioridad.
            for columna in range(len_order):
                # Se obtiene el ancho medio del espacio de las columnas disponibles.
                ancho_medio = get_ancho_medio(remaining_space, len_order)

                # Si maximo[columna] es menor al ancho medio se asigna ese valor.
                if maximos[columna] < ancho_medio:
                    anchos[columna] = maximos[columna]
                    if maximos[columna] < self.show_width_threshold:
                        maxima_less_than_show_width_threshold.append(columna)
                # Si maximo[columna] es mayor el ancho pasa a ser igual a ancho_medio.
                else:
                    anchos[columna] = ancho_medio

                # Se recalcula remaining_space.
                remaining_space -= anchos[columna]
                # Se resta una columna.
                len_order -= 1

            # Se da por finalizado el proceso de reparto, aun asi, el chequeo puede volver a poner no_finalizado en True.
            no_finalizado = False

            len_anchos = len(anchos)
            # --- Si hay anchos asignados. ---#
            # Se pone mayor a 1, para que, en caso de que solo quede una columna en pantalla, esta desobedezca 
            #    el ancho_medio menor a maximo[columna], recortando igual.
            if len_anchos > 1:
                # Se chequea si hay elementos bajo show_ancho_threshold, si es asi, y este no esta en 
                #    maxima_less_than_show_width_threshold no_finalizado = True.
                for columna in range(len_anchos):
                    if anchos[columna] < self.show_width_threshold:
                        if columna not in maxima_less_than_show_width_threshold:
                            no_finalizado = True

            if no_finalizado:
                # Se determina el indice a eliminar (indicado por el ultimo elemento de ordered_lista_prioridades).
                indice_a_eliminar = ordered_lista_prioridades[len_order - 1]
                # Al orden se le remueve el indice a eliminar.
                orden.pop(indice_a_eliminar)
                # A maximos se le remueve el indice a eliminar
                maximos.pop(indice_a_eliminar)
                # A ordered_lista_prioridades se le remueve el ultimo elemento (la menor prioridad), y se lo comprime 
                #     (para asegurar la integridad de las columnas a las cuales apunta la lista).
                ordered_lista_prioridades = widgets.compress_lista(ordered_lista_prioridades[0:len_order - 1])
                # Se recalcula len_order
                len_order = len(ordered_lista_prioridades)

        return anchos, orden


    def generar_cuadros_pantalla(self, ordered_data=None, ancho=None, maximo=None, screen_y=None):
        # --- Si no se proveen datos, retorna una lista vacia --- #
        if ordered_data == None:
            errores.append('Recordset > Render > generar_cuadros: No se proveyo ordered_data.')
            return []

        # --- Si no se provee ancho de columnas, se retorna una lista vacia --- #
        if ancho == None:
            errores.append('Recordset > Render > generar_cuadros: No se proveyo ancho_columnas.')
            return []

        # --- Si no se provee ancho de columnas, se retorna una lista vacia --- #
        if maximo == None:
            errores.append('Recordset > Render > generar_cuadros: No se proveyo maximo[].')
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
                # --- Mientras la longitud del cuadro sea mayor al ancho de la columna, este se recorta --- #
                if ancho[columna] > 0:
                    # Si ancho[columna] es igual o menor a 0, se recortara infinitamente.
                    while len(cuadro_a_recortar) > ancho[columna]:
                        cuadro.append(cuadro_a_recortar[0:after])
                        cuadro_a_recortar = cuadro_a_recortar[after:]
                # --- Si cuadro_a_recortar y ancho[columna] son iguales, se appendea el cuadro sin mas --- #
                if len(cuadro_a_recortar) == ancho[columna]:
                    cuadro.append(cuadro_a_recortar)
                # --- Si el contenido de cuadro a recortar es menor al ancho de la columna
                #     se rellena el faltante de espacios en blanco --- #
                if len(cuadro_a_recortar) < ancho[columna]:
                    cuadro.append(cuadro_a_recortar + ' ' * (ancho[columna] - len(cuadro_a_recortar)))
                # --- Se recorta el cuadro generado segun el max_y_cuadro_threshold (alto maximo) --- #
                if len(cuadro) > self.max_y_cuadro_threshold:
                    cuadro = cuadro[0:self.max_y_cuadro_threshold]

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


    # Esta funcion une las casillas intercalandoles el separador.
    def generar_pantalla(self, linea_cuadros=None, separador=None):
        if linea_cuadros == None:
            return 'Recordset > Render > generar_pantalla: No se proveyo linea_cuadros.'

        if separador == None:
            errores.append('Recordset > Render > generar_pantalla: No se proveyo separador.')
            separador = ' '

        pre_pantalla = ''
        # --- Para cada tupla de linea_cuadros. --- #
        for tupla in range(len(linea_cuadros)):
            la_tupla = linea_cuadros[tupla]
            if len(la_tupla) > 0:
                # Para cada linea en el numero que equivale al alto de la fila en la tabla.
                for linea in range(len(la_tupla[0])):
                    # --- Para cada cuadro se retirara una linea --- #
                    for cuadro in la_tupla:
                        pre_pantalla += separador + cuadro[linea]

                    pre_pantalla += '\n'

        # Si pre_pantalla termina con \n (ENTER) se retira ese ultimo ENTER.
        if len(pre_pantalla) > 0:
            if pre_pantalla[len(pre_pantalla) - 1] == '\n':
                pre_pantalla = pre_pantalla[0:len(pre_pantalla) - 1]

        return pre_pantalla


    # Esta funcion chequea que la lista de etiquetas este en orden, si no es asi intenta reconstruirla.
    def check_lista_etiquetas(self, lista_etiquetas=None, lista_tipo_datos=None, ancho=None, orden=None, separador=None):
        # Si lista_etiquetas es False, se retorna, ya que este valor tiene validez en otras partes del programa.
        if lista_etiquetas == False:
            return lista_etiquetas

        # Lista de elementos que deben intentar ser reconstruidos #
        to_rebuild = []
        # Si lista etiquetas es invalida, se reconstruye.
        if not isinstance(lista_etiquetas, list):
            errores.append('Recordset > Render > check_lista_etiquetas: lista_etiquetas no fue provista o es invalida.')
            lista_etiquetas = []
            for x in range(len(lista_tipo_datos)):
                lista_etiquetas.append(None)

        for x in range(len(lista_etiquetas)):
            if not isinstance(lista_etiquetas[x], str) or lista_etiquetas[x] == None:
                to_rebuild.append(x)
                lista_etiquetas[x] = None

        if separador == None:
            errores.append('Recordset > Render > check_lista_etiquetas: No se proveyo separador.')
            separador = ' '

        # Si la lista de etiquetas tiene mas elementos que elementos lista_tipo_datos, lista_etiquetas se recorta.
        if len(lista_etiquetas) > len(lista_tipo_datos):
            lista_etiquetas = lista_etiquetas[0:len(lista_tipo_datos)]
            errores.append('Recordset > Render > check_lista_etiquetas_integrity: Fue necesario acortar lista_etiquetas.')
        # Si es menor, se agrega None a lista_etiquetas.
        elif len(lista_etiquetas) < len(lista_tipo_datos):
            errores.append('Recordset > Render > check_lista_etiquetas_integrity: lista_etiquetas es muy corta.')
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
                etiqueta = 'Col.' + str(x)

            # Se asigna el tipo averiguado a la lista_tipo_datos
            lista_etiquetas[x] = etiqueta

        if len(to_rebuild) > 0:
            errores.append('Recordset > Render > check_lista_etiquetas: Fue necesario reconstruir lista_etiquetas.')

        if not isinstance(orden, list):
            errores.append('Recordset > Render > check_lista_etiquetas: No se proveyo orden o este es invalido.')
            ordered_lista_etiquetas = lista_etiquetas
        else:
            ordered_lista_etiquetas = []
            for elemento in orden:
                try:
                    ordered_lista_etiquetas.append(lista_etiquetas[elemento])
                except:
                    errores.append('Recordset > Render > check_lista_etiquetas: Error al intentar reordenar las etiquetas.')

        # Si no se proveen anchos, se emite un error y se retorna lista_etiquetas.
        if ancho == None:
            errores.append('Recordset > Render > check_lista_etiquetas: No se proveyo lista ancho (lista de anchos).')
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


    def post_render(self, pantalla=None, lista_etiquetas=None, len_separador=None):
        # Si no se provee pantalla.
        if pantalla == None:
            errores.append('Recordset > Render > post_render: No se proveyo pantalla, esto pasa si los datos no son validos.')

        # Si separador no es provisto, genera uno y emite un error.
        if len_separador == None:
            errores.append('Recordset > Render > post_render: No se proveyo separador.')
            len_separador = 1

        # Si lista_etiquetas no es provista, se asigna una cadena vacia.
        if lista_etiquetas == None:
            errores.append('Recordset > Render > post_render: No se proveyo lista_etiquetas.')
            lista_etiquetas = False

        # Variable que almacena la tabla renderizada.
        post_renderizado = ''

        # Si lista_etiquetas no es False, se añade a post_renderizado.
        if lista_etiquetas != False and self.show_etiquetas == True:
            post_renderizado += '\x1b[1;33m' + lista_etiquetas + '\x1b[0;99m' + '\n'

        # Se añade el render de la pantalla a post_renderizado.
        post_renderizado += pantalla + '\x1b[0;99m'
        # Si en la configuracion se especifica que se debe mostrar errores.
        if self.show_errores and len(errores) > 0:
            post_renderizado += '\n' * 2 + ' ' + ' ' * (len_separador - 1) + '\x1b[1;36mRecordset > Render > Errores > ' + widgets.actual_date() + ' ' + widgets.actual_hour() + '\x1b[0;91m\n'
            for x in range(len(errores)): 
                post_renderizado += ' ' * len_separador + errores[x] + '\n'

            # Si post_renderizado termina con \n (ENTER) se retira ese ultimo ENTER.
            if post_renderizado[len(post_renderizado) - 1] == '\n':
                post_renderizado = post_renderizado[0:len(post_renderizado) - 1]

            post_renderizado += '\x1b[0;99m'

        # Si en la configuracion se especifica que se deben registrar los errores.
        if self.log_errores:
            widgets.write_log('Recordset > Render > Errores > ' + widgets.actual_date() + ' ' + widgets.actual_hour() + ' -\n' + '\n'.join(errores))

        return post_renderizado



class Oneline:
    """
    Oneline es una clase que esta preparada para hacer impresiones linea a linea. 
    - Al igual que con Recordset se usa objeto.render(DATOS), 
    - Para esta funcion es altamente recomendable que los parametros de ancho esten bien asignados.
    - Oneline crea una instancia de Recordset, configurandola de manera que trabaje linea por linea.
    """
    def __init__(self):
        # Se genera el objeto renderizador.
        self.renderizador = Recordset()
        self.renderizador.set_log_errores(False)
        self.renderizador.set_show_errores(False)
        self.renderizador.set_check_dimensiones(True)
        self.renderizador.set_cantidad_maxima_filas(1)

    def set_check_data(self, x=True):
        self.renderizador.check_data = x

    def set_corrector(self, x=-2):
        self.renderizador.corrector = x

    def set_max_y_cuadro_threshold(self, x=20):
        self.renderizador.max_y_cuadro_threshold = x

    def set_show_ancho_threshold(self, x=True):
        self.renderizador.show_ancho_threshold = x

    def set_show_errores(self, x=True):
        self.renderizador.show_errores = x

    def set_log_errores(self, x=True):
        self.renderizador.log_errores = x

    def set_cantidad_maxima_filas(self, x=1):
        self.renderizador.cantidad_maxima_filas = x


    def show_check_data(self):
        print(self.renderizador.check_data)

    def show_corrector(self):
        print(self.renderizador.corrector)

    def show_max_y_cuadro_threshold(self):
        print(self.renderizador.max_y_cuadro_threshold)

    def show_show_ancho_threshold(self):
        print(self.renderizador.show_ancho_threshold)

    def show_show_errores(self):
        print(self.renderizador.show_errores)

    def show_log_errores(self):
        print(self.renderizador.log_errores)

    def show_cantidad_maxima_filas(self):
        print(self.renderizador.cantidad_maxima_filas)


    def render(self, data=None, anchos=None, separador=None, orden=None, lista_prioridades=None):
        """Funcion que imprime una linea por vez, en base a los datos provistos"""
        # --- Si los datos son provistos, se preparan para su renderizado. ---
        if data == None:
            return '--- Oneline > Render: No se han recibido datos para imprimir --- '
        else:
            if isinstance(data, (list, tuple)):
                if len(data) > 0:
                    # Si el contenido del primero elemento de los datos no es una tupla.
                    if not isinstance(data[0], tuple):
                        # Se insertan los datos convertidos a tupla en una lista vacia.
                        new_data = []
                        new_data.append(tuple(data))
                    else:
                        new_data = data
                else:
                    new_data = data

            # Se renderizan los datos preparados. (Hay que tener en cuenta que Recordset aplicara sus propios chequeos).
            return self.renderizador.render(new_data, separador, False, orden, None, lista_prioridades, anchos)



class Grafica:
    """
    Funcion en desarrollo.
    Inspirarse en graficas de Gnumeric(diseño) y el codigo de Matplotlib (funcionamiento).
    """
    def __init__(self):
        self.max_heigth_margin_down = 5
        self.max_width_margin_left = 10 

    def area(self, tabla, etiquetas_x):
        pass

    def barras(self, tabla):
        pass

    def columnas(self, tabla):
        pass

    def linea(self, tabla=None, etiquetas_x=None):
        # Se lleva a cabo el chequeo de datos.
        if not self.check_data_integrity(tabla):
            return '--- Grafica > Linea > Los datos ingresados son invalidos. ---'

        ##############################
        # --- AREA DE PRE-RENDER --- #
        ##############################
        # --- Se analizan las dimensiones de la pantalla --- #
        self.screen_x, self.screen_y = widgets.measure_screen()
        # --- Se obtiene el rango en el que opera la tabla --- #
        self.minimo, self.maximo, self.rango = self.get_rango(tabla)
        # --- Se asignan las letras para cada elemento de la tabla --- #
        self.letras_asignadas = self.asign_letras(tabla)

        print('--- DEVELOPMENT ---')
        print('screen_x, screen_y', screen_x, screen_y)
        print('minimo', minimo, 'maximo', maximo, 'rango', rango)
        print('letras_asignadas', letras_asignadas)


        
        '''
            Renderizar.
            Como?

            - Se analizan los datos para obtener el rango numerico de operacion.
                Como? (Buscando el maximo y el minimo numero entre TODOS los elementos de la tabla).
            - Se asignan letras de relleno para cada elemento.
            - Se determinan los margenes y espacios necesarios para representar los elementos y las etiquetas.
            - Se determina el lugar de paso de la linea.
            - Se renderiza la pre_tabla.
            - Se post_renderiza la tabla.
        '''

    def torta(self, linea):
        pass

    def anillo(self, tabla):
        pass

    def dropbar(self, linea):
        pass


    def test(self):
        # Funcion de demostracion.
        tabla = [(100, 200, 150), (200, 160, 300), (230, 170, 280)]
        input('--- Presione ENTER para ver la tabla tal cual es ---')
        print(tabla)
        input('--- Ahora presione ENTER para ver la tabla renderizada por Outfancy ---')
        print('--- GRAFICO DE LINEAS ---')
        print(self.linea(tabla))

    def check_data_integrity(self, tabla):
        error = False
        # Se chequean los datos de la tabla.
        if isinstance(tabla, list):
            len_fila = len(tabla[0])
            # Se chequean las filas de la tabla.
            for fila in tabla:
                if isinstance(fila, tuple):
                    # Si la longitud de la fila es distinta a la longitud medida inicialmente.
                    if len(fila) != len_fila:
                        error = True
                    # Para cada elemento de las filas.
                    for elemento in fila:
                        # El elemento es valido si es un entero o es nulo.
                        if not isinstance(elemento, int) or elemento != None:
                            error = True
                else:
                    error = True
        else:
            error = True

        return error


    def get_rango(self, tabla):
        # Se obtiene el valor maximo existente en la tabla.
        maximo = max(max(tabla))
        # Se obtiene el valor minimo existente en la tabla.
        minimo = min(min(tabla))
        # Se calcula el rango de valores que la tabla tiene.
        rango = maximo - minimo

        return minimo, maximo, rango


    def asign_letras(self, tabla):
        # Si la tabla tiene elementos.
        letras_asignadas = []
        if len(tabla) > 0:
            # A cada entidad a representar en la grafica se le asigna una letra.
            for elemento in range(len(tabla[0])):
                letras_asignadas.append(minus_letters[elemento])

        return letras_asignadas


    def generar_margen_izq(self):
        """Genera el margen izquierdo, con sus etiquetas, medidas y valores, que seran usados posteriormente en el render."""
        # Define el alto de la tabla.
        alto = self.screen_y - self.max_heigth_margin_down
        # Obtiene el porcentaje que representa el rango frente a (alto_pantalla - alto_maximo_margen_inferior).
        porcentaje_rango_en_screen_y = self.rango * 100 / alto
        # Obtiene el orden numerico que tendra cada espacio.
        orden_numerico = len(str(porcentaje_rango_en_screen_y))
        # Obtiene el numero de unidades por intervalo, y lo redondea.
        unidades_por_espacio = round(self.rango / alto)

        lista_etiquetas_y = []
        for x in range(0, self.rango):
            # A lista etiquetas y se le añaden las etiquetas.
            lista_etiquetas_y.append(self.minimo + (x * unidades_por_espacio))
        # El intervalo sera definido como NUMERO * MULTIPLICADOR_ORDEN.

        return lista_etiquetas_y

'''
###  PLANIFICACION Y DESARROLLO  ###

        Pseudo:
            Supongamos:
            maximo = 1234
            minimo = 1200

            screen_y = 25
            -= max_heigth_margin_down = 5
            range = 34 / 20
            etiquetas_per_pixel = 1.7

            rango = 34

            De y a y2 la resolucion es de cantidad_numeros per etiqueta.

            A calculo mental se deduce que:

            0 - 20 res. 1pp ORDEN 1

            20 - 40 res. 2pp

            40 - 100 res. 5pp

            100 - 200 res. 10pp ORDEN 2

            200 - 400 res. 20pp

            400 - 1000 res. 50pp

            1000 - 2000 res. 100pp ORDEN 3

            2000 - 4000 res. 200pp

            4000 - 10000 res. 500pp

            10000 - 20000 res. 1000pp ORDEN 4

            20000 - 40000 res. 2000pp

            40000 - 100000 res. 5000pp

            100000 - 200000 res. 10000pp ORDEN 5

            200000 - 400000 res. 20000pp

            Se calcula etiquetas_per_pixel.

            Se ajusta etiquetas_per_pixel A LA BAJA.
            En el valor mas cercano en la lista de valores.

            De la muestra se deduce que la lista de valores es - Orden 1: [1, 2, 5] - Orden 2: [1, 2, 5]

            Se deberia mostrar:
            1200, 1205, 1210 ..., 1235.

#######################################

        Pseudocodigo del algoritmo.
            1 - Se genera lista_etiquetas_y y se evalua un posible acortamiento.
                - Como?
                    - Dividir el rango por el tamaño de la pantalla.
                    - Ver si todos los elementos son divisibles entre un millon.
                    - En caso de no serlo, ver si todos los elementos son divisibles entre mil.
                    - En caso de no serlo, y ser el valor mayor a mil, ver si son divisibles entre 100.
                    - En caso de no serlo, no modificar el valor.
            2 - En caso de poder acortarse, se acorta.
            3 - Se mide el tamaño de lista_etiquetas_y,
            4 - Se retorna el ancho calculado para el margen izquierdo y la lista de etiquetas.

#######################################

Para una grafica.
A B C
1 4 7
2 5 8
3 6 9

Descripcion de la tabla.
Una tupla contiene x valores, pudiendose asignar cada valor a una y solo una entidad/motivo productor de los numeros.

Como en el ejemplo de arriba, donde en cada fila estan diferentes valores de A B C en diferentes tiempos.

tabla = [(100, 200, 300), (120, 150, 330), (110, 160, 350)]

#######################################

Falta:
    - SISTEMA DE CHEQUEO DE ANCHOS.
    - OPCION PARA ANULAR EL CHEQUEO AUTOMATICO DE ANCHOS.
'''
