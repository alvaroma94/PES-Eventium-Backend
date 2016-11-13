import psycopg2
from connection import Connection
import json
from utilsBD import UtilsBD

class CategoriesGateway:
	def __init__(self, id, categories = None):
		#variables privadas de la clase
		self.id = id
		self.categories = categories

	def remove(self):
		query = "DELETE FROM \"LIKINGS\" WHERE \"USERID\" = %s"
		values = (self.id, )
		UtilsBD.Instance().executeRemove(query,values)

	def update(self):
		self.remove()
		for c in self.categories:
			query = "INSERT INTO \"LIKINGS\" (\"USERID\", \"CATEGORYID\") VALUES (%s ,%s)"
			values = (self.id, c)
			print 'k pasa', UtilsBD.Instance().executeInsert(query,values)
		return None #siempre sale bien

	def toTuple(self):
		info = {"id" : self.id, "categories" : {}}
		return info

