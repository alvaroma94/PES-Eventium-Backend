import psycopg2
import SingletonPattern
from UserGateway import UserGateway
from connection import Connection
from utilsBD import UtilsBD
import json

#patron finder de Row Data Gateway
@SingletonPattern.Singleton
class UserFinder:
	def __init__(self):
		pass


	def find(self, username):
		query = "SELECT * FROM \"USER\" WHERE \"USERNAME\" = %s"
		values = (username,)
		t = UtilsBD.Instance().executeSelect(query, values, fetchone = True)
		if (t):
			user = UserGateway(id = t[0], username = t[1], password = t[2])
			return user
		return t
	def findByMailOrUser(self, clave):

		query = "SELECT * FROM \"USER\" WHERE \"USERNAME\" = %s or  \"MAIL\" = %s"
		values = (clave, clave)
		t = UtilsBD.Instance().executeSelect(query, values, fetchone = True)
		if (t):
			user = UserGateway(id = t[0], username = t[1], password = t[2], mail = t[3])
			return user
		return t

