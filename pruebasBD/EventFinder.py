import psycopg2
import SingletonPattern
from EventGateway import EventGateway
from connection import Connection
from utilsBD import UtilsBD
import json

#patron finder de Row Data Gateway
@SingletonPattern.Singleton
class EventFinder:
	def __init__(self):
		pass

	def getAll(self,fecha_ini, fecha_fin, hora_ini, hora_fin, titulo ,precioMin , precioMax,ciudad,categoria):
		cont = 0
		if fecha_ini != None: cont = cont + 1
		if fecha_fin != None: cont = cont + 1
		if hora_ini != None: cont = cont + 1
		if hora_fin != None: cont = cont + 1
		if titulo != None: cont = cont + 1
		if precioMin != None: cont = cont + 1
		if precioMax != None: cont = cont + 1
		if ciudad != None: cont = cont + 1
		if categoria != None: cont = cont + 1


		if cont == 0 :
			query = "SELECT * FROM \"EVENT\" "
		else :
			query = "SELECT * FROM \"EVENT\" WHERE"


		if ciudad != None:
			cont = cont - 1
			if cont == 0:
				query = query + " \"CIUDAD\" ILIKE '%s' " % (ciudad)
			elif cont > 0:
				query = query + " \"CIUDAD\" ILIKE '%s' AND" % (ciudad)

		if precioMin != None:
			cont = cont - 1
			if cont == 0:
				query = query + " \"PRECIO\" >= '%s' " % (precioMin)
			elif cont > 0:
				query = query + " \"PRECIO\" >= '%s' AND" % (precioMin)

		if precioMax != None:
			cont = cont - 1
			if cont == 0:
				query = query + " \"PRECIO\" <= '%s' " % (precioMax)
			elif cont > 0:
				query = query + " \"PRECIO\" <= '%s' AND" % (precioMax)

		if titulo != None:
			cont = cont - 1
			if cont == 0:
				query = query + " \"TITULO\" ILIKE '%s' " % (titulo)
			elif cont > 0:
				query = query + " \"TITULO\" ILIKE '%s' AND" % (titulo)

		if fecha_ini != None:
			cont = cont - 1
			if cont == 0:
				query = query + " \"FECHA_INI\" >= '%s' " % (fecha_ini)
			elif cont > 0:
				query = query + " \"FECHA_INI\" >= '%s' AND" % (fecha_ini)

		if fecha_fin != None:
			cont = cont - 1
			if cont == 0:
				query = query + " \"FECHA_FIN\" <= '%s' " % (fecha_fin)
			elif cont > 0:
				query = query + " \"FECHA_FIN\" <= '%s' AND" % (fecha_fin)

		if hora_fin != None:
			cont = cont - 1
			if cont == 0:
				query = query + " \"HORA_FIN\" <= '%s' " % (hora_fin)
			elif cont > 0:
				query = query + " \"HORA_FIN\" <= '%s' AND" % (hora_fin)

		if hora_ini != None:
			cont = cont - 1
			if cont == 0:
				query = query + " \"HORA_INI\" >= '%s' " % (hora_ini)
			elif cont > 0:
				query = query + " \"HORA_INI\" >= '%s' AND" % (hora_ini)

		if categoria != None:
			cont = cont - 1
			if cont == 0:
				query = query + " \"CATEGORIA\" >= '%s' " % (categoria)
			elif cont > 0:
				query = query + " \"CATEGORIA\" >= '%s' AND" % (categoria)


		tuples = UtilsBD.Instance().executeSelect(query, None, fetchone = False)
		ret = []
		for t in tuples:
			test = EventGateway(id = t[0], organizerId = t[1], title = t[2], horaf = t[6], horai = t[5],  fechaf = t[4], fechai = t[3],  precio = t[7],  pic = t[8],  ciudad = t[9], categoria = t[10], destacado = t[11])
			ret.append(test)
		return ret

	def getTitulo(self, titulo):
		query = "SELECT * FROM \"EVENT\" WHERE \"TITLE\" = %s"
		values = (titulo,)
		tuples = UtilsBD.Instance().executeSelect(query, values, fetchone = False)
		ret = []
		for t in tuples:
			test = EventGateway(id = t[0], organizerId = t[1], title = t[2])
			ret.append(test)
		return ret

	def findById(self, id):
		query = "SELECT * FROM \"EVENT\" WHERE \"ID\" = %s"
		values = (id,)
		tuples = UtilsBD.Instance().executeSelect(query, values, fetchone = False)
		ret = []
		for t in tuples:
			test = EventGateway(id = t[0], organizerId = t[1], title = t[2], horaf = t[6], horai = t[5],  fechaf = t[4], fechai = t[3],  precio = t[7],  pic = t[8],  ciudad = t[9], categoria = t[10], destacado = t[11])
			return test
		return ret

	def getAllDestacados(self):
		query = "SELECT * FROM \"EVENT\" WHERE \"DESTACADO\" = True"
		tuples = UtilsBD.Instance().executeSelect(query, None, fetchone = False)
		ret = []
		for t in tuples:
			test = EventGateway(id = t[0], organizerId = t[1], title = t[2], horaf = t[6], horai = t[5],  fechaf = t[4], fechai = t[3],  precio = t[7],  pic = t[8],  ciudad = t[9], categoria = t[10], destacado = t[11])
			ret.append(test)
		return ret

	def findByUserId(self, id):
		query = "SELECT * FROM \"EVENT\" WHERE \"ORGANIZERID\" = %s"
		values = (id,)
		tuples = UtilsBD.Instance().executeSelect(query, values, fetchone = False)
		ret = []
		for t in tuples:
			test = EventGateway(id = t[0], organizerId = t[1], title = t[2], horaf = t[6], horai = t[5],  fechaf = t[4], fechai = t[3],  precio = t[7],  pic = t[8],  ciudad = t[9], categoria = t[10], destacado = t[11])
			ret.append(test)
		return ret

	# categories tiene q ser un array []
	def findByCategories(self,categories):
		query = "SELECT * FROM \"EVENT\" WHERE \"CATEGORIA\" = ANY(%s)"
		values = (categories,)
		print values
		tuples = UtilsBD.Instance().executeSelect(query, values, fetchone = False)
		ret = []
		for t in tuples:
			test = EventGateway(id = t[0], organizerId = t[1], title = t[2], horaf = t[6], horai = t[5],  fechaf = t[4], fechai = t[3],  precio = t[7],  pic = t[8],  ciudad = t[9], categoria = t[10], destacado = t[11])
			ret.append(test)
		return ret