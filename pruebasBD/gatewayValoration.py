import psycopg2
from connection import Connection
import json
from utilsBD import UtilsBD

#patron row data gateway (cada instancia de la clase es una fila de la bd)
class GatewayValoration:
	def __init__(self, points, userid, eventid):
		#variables privadas de la clase
		self.points = points
		self.userid = userid
		self.eventid = eventid

	def insert(self):
		query = "INSERT INTO \"VALORATION\" (\"POINTS\", \"USERID\", \"EVENTID\") VALUES (%s ,%s, %s)"
		values = (self.points, self.userid, self.eventid)
		return UtilsBD.Instance().executeInsert(query,values)
	def update(self):
		pass

	def toTuple(self):
		info = {"points" : self.points, "userid" : self.userid, "eventid":self.eventid}
		return info

class GatewayVoted(GatewayValoration):
	def toTuple(self):
		if self.points != None and self.userid != None:
			voted = 'True'
		else: voted = 'False'
		return {"voted": voted}