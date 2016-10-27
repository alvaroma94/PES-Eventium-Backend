import psycopg2
import SingletonPattern
from gatewayFollowing import GatewayFollowing
from connection import Connection
from utilsBD import UtilsBD
import json

@SingletonPattern.Singleton
class FinderFollowing:
	def __init__(self):
		pass
	def findSubscription(self, id, followed):
		query = "SELECT * FROM \"FOLLOWS\" WHERE \"FOLLOWERID\" = %s and \"FOLLOWEDID\" = %s"
		values = (id,followed)
		t = UtilsBD.Instance().executeSelect(query, values, fetchone = True)
		if (t):
			test = GatewayFollowing(t[0], t[1])
			return test
		return t

