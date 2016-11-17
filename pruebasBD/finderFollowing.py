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
	def find(self,id):
		query = "SELECT * FROM \"FOLLOWS\" WHERE \"FOLLOWERID\" = %s"
		values = (id,)
		tuples = UtilsBD.Instance().executeSelect(query, values, fetchone = False)
		ret = []
		for t in tuples:
			test = GatewayFollowing(followerId = t[0], followedId = t[1], subscribed = t[2])
			ret.append(test)
		return ret

	def findSubscription(self, id, followed):
		query = "SELECT * FROM \"FOLLOWS\" WHERE \"FOLLOWERID\" = %s and \"FOLLOWEDID\" = %s"
		values = (id,followed)
		t = UtilsBD.Instance().executeSelect(query, values, fetchone = True)
		if (t):
			test = GatewayFollowing(t[0], t[1])
			return test
		return t
		

