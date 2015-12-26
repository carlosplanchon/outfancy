#!/usr/bin/python3
# -*- coding: utf-8 -*-

import widgets, render_functions

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
            if render_functions.check_data_integrity(data):
                return '--- Render > check_data_integrity: Dato invalido o no integro ---'

        ##############################
        # --- AREA DE PRE-RENDER --- #
        ##############################
        # --- Se analizan las dimensiones de la pantalla --- #
        screen_x, screen_y = widgets.medir_dimensiones()
        # --- Se aplica valor de correccion a screen_x --- #
        screen_x += self.corrector
        # --- Se chequea el separador --- #
        separador = render_functions.check_separador(separador, screen_x)
        # --- Se chequea la validez del orden provisto --- #
        orden = render_functions.check_orden(data, orden)
        # --- Se reordenan los datos y las etiquetas --- #
        ordered_data = render_functions.reordenar_datos(data, orden)
        # --- Chequea la longitud maxima para mostrar cada campo de ordered_data --- #
        maximo = render_functions.check_maximos(ordered_data)
        # --- Se chequea la integridad de la lista de tipos de datos --- #
        lista_tipo_datos = render_functions.check_lista_tipo_datos_integrity(self.analyze_threshold, data, lista_tipo_datos)
        # --- Se reordena lista_tipo_datos --- #
        ordered_lista_tipo_datos = render_functions.reordenar_lista_tipo_datos(lista_tipo_datos, orden)
        ##########################
        # --- AREA DE RENDER --- #
        ##########################
        # --- Asigna el ancho para mostrar las columnas, si este no es provisto, intenta deducirlo --- #
        ordered_lista_tipo_datos, cadena_prioridades, ancho = render_functions.asign_ancho_columnas(self.show_ancho_thresholding, maximo, screen_x, ordered_lista_tipo_datos, cadena_prioridades, len(separador), orden)
        # --- Genera las casillas que contienen los datos --- #
        linea_cuadros = render_functions.generar_cuadros_pantalla(self.max_y_cuadro_threshold, ordered_data, ancho, maximo, screen_y)
        # --- Genera el area de la pantalla que contiene el pre_render del recordset --- #
        pantalla = render_functions.generar_pantalla(linea_cuadros, separador)
        # --- Chequea que la lista de etiquetas este en orden, si no es asi intenta deducirlas --- #
        lista_etiquetas = render_functions.check_lista_etiquetas(lista_etiquetas, lista_tipo_datos, ancho, orden, separador)
        ###############################
        # --- AREA DE POST-RENDER --- #
        ###############################
        # --- Lleva a cabo el post_render, uniendo el pre_render del recordset con los demas datos --- #
        return render_functions.post_render(self.show_errores, self.log_errores, pantalla, lista_etiquetas, len(separador))
