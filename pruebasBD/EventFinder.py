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

	def getAll(self):
		query = "SELECT * FROM \"EVENT\""
		tuples = UtilsBD.Instance().executeSelect(query, None, fetchone = False)
		ret = []
		for t in tuples:
			test = EventGateway(id = t[0], organizerId = t[1], title = t[2], horaf = t[6], horai = t[5],  fechaf = t[4], fechai = t[3],  precio = t[7],  pic = t[8],  ciudad = t[9])
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
	