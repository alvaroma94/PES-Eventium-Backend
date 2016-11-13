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

	def findForDeposit(self, id):
		query = "SELECT \"SALDO\" FROM \"USER\" WHERE \"ID\" = %s"
		values = (id,)
		t = UtilsBD.Instance().executeSelect(query, values, fetchone = True)
		if (t):
			print t
			user = UserGateway(id = id, username = None, password = None, mail = None, wallet = t[0])
			return user
		return t

	def findByName(self, username):
		query = "SELECT * FROM \"USER\" WHERE \"USERNAME\" = %s"
		values = (username,)
		t = UtilsBD.Instance().executeSelect(query, values, fetchone = True)
		if (t):
			user = UserGateway(id = t[0], username = t[1], password = t[2], mail = t[3], pic = t[6], verified = t[7])
			return user
		return t

	def getAll(self):
		query = "SELECT * FROM \"USER\""
		tuples = UtilsBD.Instance().executeSelect(query, None, fetchone = False)
		ret = []
		for t in tuples:
			test = UserGateway(id = t[0], username = t[1], password = t[2], mail = t[3], pic = t[6], verified = t[7])
			ret.append(test)
		return ret

	def findByMailOrUser(self, clave):

		query = "SELECT * FROM \"USER\" WHERE \"USERNAME\" = %s or  \"MAIL\" = %s"
		values = (clave, clave)
		t = UtilsBD.Instance().executeSelect(query, values, fetchone = True)
		if (t):
			user = UserGateway(id = t[0], username = t[1], password = t[2], mail = t[3], pic = t[6], verified = t[7])
			return user
		return t

	def findForLogin(self, username, password):
		query = "SELECT * FROM \"USER\" WHERE \"USERNAME\" = %s and  \"PASSWORD\" = %s"
		values = (username, password)
		t = UtilsBD.Instance().executeSelect(query, values, fetchone = True)
		if (t):
			user = UserGateway(id = t[0], username = t[1], password =None, mail = t[3], pic = t[6])
			return user
		return t

	def findById(self, id):
		query = "SELECT * FROM \"USER\" WHERE \"ID\" = %s"
		values = (id,)
		t = UtilsBD.Instance().executeSelect(query, values, fetchone = True)
		if (t):
			user = UserGateway(id = t[0], username = t[1], password =t[2], mail = t[3], pic = t[6], verified = t[7])
			return user
		return t