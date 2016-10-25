import psycopg2
import SingletonPattern
from gatewayComment import GatewayComment
from connection import Connection
from utilsBD import UtilsBD
import json

#patron finder de Row Data Gateway
@SingletonPattern.Singleton
class FinderComment:
	def __init__(self):
		pass
	def findByEvent(self, eventid):
		query = "SELECT * FROM \"COMMENT\" WHERE \"EVENTID\" = %s"
		values = (eventid,)
		t = UtilsBD.Instance().executeSelect(query, values, fetchone = False)
		if (t):
			comment = GatewayComment(text = t[0], userid = t[1], eventid = t[2])
			return comment
		return t