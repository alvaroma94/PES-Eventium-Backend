import psycopg2
from connection import Connection
import json

#patron row data gateway (cada instancia de la clase es una fila de la bd)
class GatewayTest:
	def __init__(self, id, num, data):
		#variables privadas de la clase
		self.id = id
		self.num = num
		self.data = data
	def getId(self):
		return self.id

	def getNum(self):
		return self.num

	def getData(self):
		return self.data

	def insert(self):
		ret = True
		try:
			c = Connection.Instance()
			cursor = c.cursor()
			query = "INSERT INTO test (id, num, data) VALUES (%s ,%s, %s)"
			values = (self.id, self.num, self.data)
			cursor.execute(query, values)
			c.commit()
			cursor.close()
		except psycopg2.IntegrityError as err:
			print err
			ret = False
			c.rollback()
		return ret


	def remove(self):
		c = Connection.Instance()
		cursor = c.cursor()
		query = "DELETE FROM test WHERE id = %s"
		values = (self.id,)
		cursor.execute(query, values)
		c.commit()
		cursor.close()
		
	def update(self):
		c = Connection.Instance()
		cursor = c.cursor()
		query = "UPDATE test SET num = %s, data = %s WHERE id = %s" 
		values = (self.num, self.data, self.id)
		cursor.execute(query, values)
		c.commit()
		cursor.close()

	def toTuple(self):
		info = {"id" : self.id, "num" : self.num, "data" : self.data}
		return info


