import psycopg2
from connection import Connection
import json
from utilsBD import UtilsBD

class SponsoredGateway:
	def __init__(self, sponsorid, eventid):
		self.sponsorid = sponsorid
		self.eventid = eventid
	def insert(self):
		query = "INSERT INTO \"SPONSORED\" (\"USERID\",\"EVENTID\") VALUES (%s,%s)"
		values = (self.sponsorid, self.eventid)
		return UtilsBD.Instance().executeInsert(query,values)