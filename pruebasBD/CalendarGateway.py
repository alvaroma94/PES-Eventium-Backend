import psycopg2
from connection import Connection
import json
from utilsBD import UtilsBD

#patron row data gateway (cada instancia de la clase es una fila de la bd)
class CalendarGateway:

	def __init__(self, userid, eventid, fecha):
		self.userid = userid
		self.eventid = eventid
		self.fecha = fecha

	def insert(self):
		query = "INSERT INTO \"CALENDAR\"   (\"USERID\" , \"EVENTID\" , \"FECHA\") VALUES (%s, %s, %s)"
		values = (self.userid, self.eventid, self.fecha)
		return UtilsBD.Instance().executeInsert(query,values)

	def delete(self):
		pass
