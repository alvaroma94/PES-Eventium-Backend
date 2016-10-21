import psycopg2
import SingletonPattern
from gatewayTest import GatewayTest
from connection import Connection
from utilsBD import UtilsBD
import json

#patron finder de Row Data Gateway
@SingletonPattern.Singleton
class FinderTest:
	def __init__(self):
		pass
	def find(self, id):
		query = "SELECT * FROM test WHERE id = %s"
		values = (id,)
		t = UtilsBD.Instance().executeSelect(query, values, fetchone = True)
		if (t):
			test = GatewayTest(id = t[0], num = t[1], data = t[2])
			return test
		return t

	def getAll(self):
		query = "SELECT * FROM test"
		tuples = UtilsBD.Instance().executeSelect(query, None, fetchone = False)
		ret = []
		for t in tuples:
			test = GatewayTest(id = t[0], num = t[1], data = t[2])
			ret.append(test)
		return ret

	
