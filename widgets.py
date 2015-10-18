#!/usr/bin/python3
# -*- coding: utf-8 -*-

import string
from time import strptime
from datetime import datetime
from os import path, system

def check_inicio():
	if not path.exists('registro.log'):
		system('touch registro.log')

def list_join(lista_comando):
	return ' '.join(lista_comando)

def escribirarchivo(namearchivo, cadena):
	archivo = open(namearchivo, 'w')
	archivo.write(cadena)
	archivo.close()

def leerarchivo(namearchivo):
	archivo = open(namearchivo, 'r')
	contenido = archivo.read()
	archivo.close()
	return contenido

def write_log(text):
	log = leerarchivo('registro.log')
	escribirarchivo('registro.log', log + '\n' + text)

def check_isnumerico(text):
	try:
		text = str(int(text))
		return True
	except:
		return False

#Esta funcion quita el formato relajado de las fechas
def text_desrelajar(text):
	text = text.replace('/','-')
	text = text.replace(':','-')
	text = text.replace('.','-')
	text = text.replace('@','-')
	return text

def isfecha(text):
	text = text_desrelajar(text)
	for format in ['%d-%m-%Y', '%d-%m-%y', '%d-%m-%Y %H-%M-%S', '%d-%m-%y %H-%M-%S']:
		try:
			strptime(text, format)
			return True	
		except:
			pass
	return False

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
