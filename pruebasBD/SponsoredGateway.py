import psycopg2
from connection import Connection
import json
from utilsBD import UtilsBD

class SponsoredGateway:
	def __init__(self, sponsorid, eventid):
		self.sponsorid = sponsorid
		self.eventid = eventid
	def delete(self):
		query = "DELETE FROM \"SPONSORED\" WHERE \"USERID\" = %s and \"EVENTID\" = %s"
		values = (self.sponsorid,self.eventid)
		return UtilsBD.Instance().executeRemove(query,values)
	def insert(self):
		query = "INSERT INTO \"SPONSORED\" (\"USERID\",\"EVENTID\") VALUES (%s,%s)"
		values = (self.sponsorid, self.eventid)
		return UtilsBD.Instance().executeInsert(query,values)
	def toTuple(self):
		return {'userid':self.sponsorid,'eventid':self.eventid}