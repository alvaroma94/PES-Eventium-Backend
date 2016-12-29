import psycopg2
import SingletonPattern
from CalendarGateway import CalendarGateway
from connection import Connection
from utilsBD import UtilsBD
import json

#patron finder de Row Data Gateway
@SingletonPattern.Singleton
class CalendarFinder:
	def __init__(self):
		pass
	def getByUserId(self, id):
		query = "SELECT * FROM \"CALENDAR\" WHERE \"USERID\" = %s"
		values = (id,)
		rows = UtilsBD.Instance().executeSelect(query, values, fetchone = False)
		ret = []
		for row in rows:
			ret.append(CalendarGateway(id, row[1]))
		return ret
	def getEntry(self,id,eventid):
		query = "SELECT * FROM \"CALENDAR\" WHERE \"USERID\" = %s and \"EVENTID\" = %s"
		values = (id,eventid)
		row = UtilsBD.Instance().executeSelect(query, values, fetchone = True)
		return CalendarGateway(id, row[1])

	def getAllByEvent(self, id):
		query = "SELECT \"USERID\" FROM \"CALENDAR\" WHERE \"EVENTID\" = %s"
		values = (id,)
		rows = UtilsBD.Instance().executeSelect(query, values, fetchone = False)
		ret = []
		for row in rows:
			ret.append(CalendarGateway(row[0], id))
		return ret