import psycopg2
from connection import Connection
import json
from utilsBD import UtilsBD

#patron row data gateway (cada instancia de la clase es una fila de la bd)
class GatewayFollowing:
	def __init__(self, followerId, followedId, subscribed = False):
		#variables privadas de la clase
		self.followedId = followedId
		self.followerId = followerId
		self.subscribed = subscribed

	def insert(self):
		query = "INSERT INTO \"FOLLOWS\" (\"FOLLOWERID\", \"FOLLOWEDID\", \"SUBSCRIBED\") VALUES (%s ,%s, %s)"
		values = (self.followerId, self.followedId, self.subscribed)
		return UtilsBD.Instance().executeInsert(query,values)
			
	def toTuple(self):
		info = {"followerId": self.followerId, "followed": self.followedId, "subscribed": self.subscribed}
		return info