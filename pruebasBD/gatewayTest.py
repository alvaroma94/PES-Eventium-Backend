import psycopg2
from connection import Connection
import json
from utilsBD import UtilsBD

#patron row data gateway (cada instancia de la clase es una fila de la bd)
class GatewayTest:
	def __init__(self, id, num, data):
		#variables privadas de la clase
		self.id = id
		self.num = num
		self.data = data

	def insert(self):
		query = "INSERT INTO test (id, num, data) VALUES (%s ,%s, %s)"
		values = (self.id, self.num, self.data)
		return UtilsBD.Instance().executeInsert(query,values)
			
	def remove(self):
		query = "DELETE FROM test WHERE id = %s"
		values = (self.id,)
		UtilsBD.Instance().executeRemove(query,values)
		
	def update(self):
		query = "UPDATE test SET num = %s, data = %s WHERE id = %s" 
		values = (self.num, self.data, self.id)
		return UtilsBD.Instance().executeUpdate(query,values)
		

	def toTuple(self):
		info = {"id" : self.id, "num" : self.num, "data" : self.data}
		return info


