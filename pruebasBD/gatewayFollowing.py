import psycopg2
from connection import Connection
import json
from utilsBD import UtilsBD

#patron row data gateway (cada instancia de la clase es una fila de la bd)
class GatewayFollowing:
	def __init__(self, followerId, followedId, subscribed = False):
		#variables privadas de la clase
		self.followerId = followerId
		self.followedId = followedId
		self.subscribed = subscribed

	def setSubscribed(subscribed):
		self.subscribed = subscribed

	def insert(self):
		query = "INSERT INTO \"FOLLOWS\" (\"FOLLOWERID\", \"FOLLOWEDID\", \"SUBSCRIBED\") VALUES (%s ,%s, %s)"
		values = (self.followerId, self.followedId, self.subscribed)
		return UtilsBD.Instance().executeInsert(query,values)
	
	def update(self):
		query = "UPDATE \"FOLLOWS\" SET \"SUBSCRIBED\" = %s WHERE \"FOLLOWERID\" = %s and \"FOLLOWEDID\" = %s"
		values = (self.subscribed, self.followerId, self.followedId)
		return UtilsBD.Instance().executeUpdate(query,values)
	
	def remove(self):
		query = "DELETE FROM \"FOLLOWS\" WHERE \"FOLLOWERID\" = %s and \"FOLLOWEDID\" = %s"
		values = (self.followerId, self.followedId)
		UtilsBD.Instance().executeRemove(query,values)
		
	def toTuple(self):
		info = {"followerId": self.followerId, "followed": self.followedId, "subscribed": self.subscribed}
		return info