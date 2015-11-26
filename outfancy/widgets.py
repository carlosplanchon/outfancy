#!/usr/bin/python3
# -*- coding: utf-8 -*-

#####################################################################################################
#                                                                                                   #
#    MODULO WIDGETS                                                                                 #
#                                                                                                   #
#    Este modulo se encarga de mostrar informacion con un buen formato                              #
#    La forma en la cual esta informacion se muestra depende del tamaño                             #
#    de la pantalla.                                                                                #
#                                                                                                   #
#    Puede recibir comandos para imprimir en formato ficha o sin formato.                           #
#    La funcion para recibir comandos es interna, y debe ser llamada                                #
#    desde el programa en si                                                                        #
#                                                                                                   #
#    INDICE DE FUNCIONES DEL MODULO                                                                 #
#---------------------------------------------------------------------------------------------------#
#                                                                                                   #
#    check_inicio()                         - Hace el chequeo inicial.                              #
#    list_join(lista_comando)               - Une una lista por espacios.                           #
#    escribirarchivo(namearchivo, cadena)   - Esta funcion escribe un archivo.                      #
#    leerarchivo(namearchivo)               - Esta funcion lee un archivo.                          #
#    write_log(text)                        - Esta funcion escribe el log.                          #
#    check_isnumerico(text)                 - Esto chequea si el ingreso es numerico.               #
#    text_desrelajar(text)                  - Esta funcion quita el formato relajado de las fechas. #
#    isfecha(text)                          - Esto chequea si lo ingresado es una fecha.            #
#    ishora_complete(text)                  - Esto chequea si lo ingresado es una hora o no.        #
#    fecha_actual()                         - Devuelve la fecha actual.                             #
#    hora_actual()                          - Devuelve la hora actual.                              #
#                                                                                                   #
#####################################################################################################

import string
from time import strptime
from datetime import datetime
from os import path, system, mkdir

#Archivo de registro.
log_file = '/tmp/outfancy/registro.log'

#Esto hace el chequeo inicial.
def check_inicio():
    if not path.exists('/tmp/outfancy'):
        mkdir('/tmp/outfancy')
    if not path.exists('/tmp/outfancy/registro.log'):
        system('touch /tmp/outfancy/registro.log')

#Esta funcion une una lista por espacios
def list_join(lista_comando):
    return ' '.join(lista_comando)

#Esta funcion escribe un archivo.
def escribirarchivo(namearchivo, cadena):
    archivo = open(namearchivo, 'w')
    archivo.write(cadena)
    archivo.close()

#Esta funcion lee un archivo.
def leerarchivo(namearchivo):
    archivo = open(namearchivo, 'r')
    contenido = archivo.read()
    archivo.close()
    return contenido

#Esta funcion escribe el log.
def write_log(text):
    log = leerarchivo(log_file)
    escribirarchivo(log_file, log + '\n' + text)

#Esto chequea si el ingreso es numerico.
def check_isnumerico(text):
    try:
        text = str(int(text))
        return True
    except:
        return False

#Esta funcion quita el formato relajado de las fechas.
def text_desrelajar(text):
    text = text.replace('/','-')
    text = text.replace(':','-')
    text = text.replace('.','-')
    text = text.replace('@','-')
    return text

#Esto chequea si lo ingresado es una fecha.
def isfecha(text):
    text = text_desrelajar(text)
    for format in ['%d-%m-%Y', '%d-%m-%y', '%d-%m-%Y %H-%M-%S', '%d-%m-%y %H-%M-%S']:
        try:
            strptime(text, format)
            return True    
        except:
            pass
    return False

#Esto chequea si lo ingresado es una hora o no.
def ishora_complete(text):
    for format in ['%H:%M:%S', '%H:%M']:
        try:
            strptime(text, format)
            return True    
        except:
            pass
    return False

#Esto devuelve la fecha actual
def fecha_actual():
    fecha_actual = datetime.now()
    return str(fecha_actual.day) + '-' + str(fecha_actual.month) + '-' + str(fecha_actual.year)

#Esto devuelve la hora actual
def hora_actual():
    hora_actual = datetime.now()
    return str(hora_actual.hour) + ':' + str(hora_actual.minute) + ':' + str(hora_actual.second)
