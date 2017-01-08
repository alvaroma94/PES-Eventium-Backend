import psycopg2
import SingletonPattern
from connection import Connection
from gatewayValoration import GatewayVoted
from utilsBD import UtilsBD
import json

@SingletonPattern.Singleton
class ValorationFinder:
	def __init__(self):
		pass

	def findVoted(self,userid,eventid):
		query =  "SELECT * FROM \"VALORATION\" WHERE \"USERID\" = %s AND  \"EVENTID\" = %s"
		values = (userid,eventid)
		t = UtilsBD.Instance().executeSelect(query, values, fetchone = True)
		if t:
			print t
			return GatewayVoted(t[0], t[1],t[2])
		else:
			return GatewayVoted(None,None,None)
