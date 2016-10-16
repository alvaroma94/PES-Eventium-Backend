import psycopg2
import SingletonPattern
from gatewayTest import GatewayTest
from connection import Connection
import json

#patron finder de Row Data Gateway
@SingletonPattern.Singleton
class FinderTest:
	def __init__(self):
		pass
	def find(self, id):
		c = Connection.Instance()
		cursor = c.cursor()
		query = "SELECT * FROM test WHERE id = %s"
		values = (id,)
		cursor.execute(query, values)
		t = cursor.fetchone()
		if (t):
			test = GatewayTest(id = t[0], num = t[1], data = t[2])
			return test
		return t

	def getAll(self):
		c = Connection.Instance()
		cursor = c.cursor()
		query = "SELECT * FROM test"
		cursor.execute(query)
		tuples = cursor.fetchall()
		ret = []
		for t in tuples:
			test = GatewayTest(id = t[0], num = t[1], data = t[2])
			ret.append(test)
		return ret

	def tupleToJson(self, info): #tuple es una palabra reservada de python
		return json.dumps(info.toTuple())

	def tuplesToJson(self, tuples):
		ret = []
		for t in tuples:
			ret.append(t.toTuple())
		return json.dumps(ret)
