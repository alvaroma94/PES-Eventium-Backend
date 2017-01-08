import psycopg2
from connection import Connection
import json
from utilsBD import UtilsBD

#patron row data gateway (cada instancia de la clase es una fila de la bd)
class GatewayComment:
	def __init__(self, text, userid, eventid):
		#variables privadas de la clase
		self.text = text
		self.userid = userid
		self.eventid = eventid

	def insert(self):
		query = "INSERT INTO \"COMMENT\" (\"TEXT\", \"USERID\", \"EVENTID\") VALUES (%s ,%s, %s)"
		values = (self.text, self.userid, self.eventid)
		return UtilsBD.Instance().executeInsert(query,values)

	def update(self):
		query = "UPDATE \"COMMENT\" SET \"TEXT\" = %s WHERE \"USERID\" = %s AND \"EVENTID\" = %s"
		values = (self.text, self.userid, self.eventid)
		return UtilsBD.Instance().executeUpdate(query,values)

	def toTuple(self):
		info = {"text" : self.text, "userid" : self.userid, "eventid":self.eventid}
		return info