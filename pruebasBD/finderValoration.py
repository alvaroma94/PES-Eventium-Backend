import psycopg2
import SingletonPattern
from gatewayValoration import GatewayValoration
from connection import Connection
from utilsBD import UtilsBD
import json

#patron finder de Row Data Gateway
@SingletonPattern.Singleton
class FinderValoration:
	def __init__(self):
		pass
	def findByEvent(self, eventid):
		query = "SELECT * FROM \"VALORATION\" WHERE \"EVENTID\" = %s"
		values = (eventid,)
		tuples = UtilsBD.Instance().executeSelect(query, values, fetchone = False)
		ret = []
		for t in tuples:
			test = GatewayComment(text = t[0], userid = t[1], eventid = t[2])
			ret.append(test)
		return ret