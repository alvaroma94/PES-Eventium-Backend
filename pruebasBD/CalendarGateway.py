import psycopg2
from connection import Connection
import json
from utilsBD import UtilsBD

#patron row data gateway (cada instancia de la clase es una fila de la bd)
class CalendarGateway:

	def __init__(self, userid, eventid):
		self.userid = userid
		self.eventid = eventid


	def insert(self):
		query = "INSERT INTO \"CALENDAR\"   (\"USERID\" , \"EVENTID\" ) VALUES (%s, %s)"
		values = (self.userid, self.eventid)
		return UtilsBD.Instance().executeInsert(query,values)

	def delete(self):
		query = "DELETE FROM \"CALENDAR\" WHERE \"USERID\" = %s and \"EVENTID\" = %s"
		values = (self.userid, self.eventid)
		UtilsBD.Instance().executeRemove(query,values)

	def toTuple(self):
		info = {"userid": self.userid, "eventid" : self.eventid}
		return info