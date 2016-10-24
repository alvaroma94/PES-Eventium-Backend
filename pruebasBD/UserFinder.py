import psycopg2
import SingletonPattern
from userGateway import userGateway
from connection import Connection
from utilsBD import UtilsBD
import json

#patron finder de Row Data Gateway
@SingletonPattern.Singleton
class UserFinder:
	def __init__(self):
		pass
	def find(self, username):
		query = "SELECT * FROM user WHERE username = %s"
		values = (username,)
		t = UtilsBD.Instance().executeSelect(query, values, fetchone = True)
		if (t):
			user = userGateway(id = t[0], username = t[1], password = t[2])
			return user
		return t
	
