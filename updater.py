#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from . import widgets

def update():
	if check_update:
		try:
			os.system('wget https://github.com/carlosplanchon/outfancy/archive/master.zip')
		except:
			return 'Error al chequear actualizacion, compruebe su conexion a internet. '
		registro = widgets.leerarchivo('outfancy/registro.log')
		os.system('unzip master.zip && rm -rf outfancy && mv outfancy-master outfancy && rm master.zip && cd outfancy && touch registro.log')
		widgets.escribirarchivo('registro.log', registro)
	return '--- Actualizado ---'

#Chequea la version, en caso de necesitar actualizacion devuelve True.
def check_update():
	os.renames('version.py', 'check_version.py')
	try:
		version_py = os.system('wget https://raw.githubusercontent.com/carlosplanchon/outfancy/master/version.py')
	except:
		print('Error al chequear actualizacion, revise su conexion a internet')
		return False
	import check_version, version
	if check_version.__version__ == version.__version__:
		need_update = False
	else:
		need_update = True
	os.remove('version.py')
	os.renames('check_version.py', 'version.py')

	return need_update
