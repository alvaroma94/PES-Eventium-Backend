import psycopg2
from connection import Connection
import json
from utilsBD import UtilsBD

#patron row data gateway (cada instancia de la clase es una fila de la bd)
class EventGateway:
	def __init__(self, id, organizerId, title):
		#variables privadas de la clase
		self.id = id
		self.organizerId = organizerId
		self.title = title

	def insert(self):
		query = "INSERT INTO \"EVENT\" (\"ORGANIZERID\", \"TITLE\") VALUES (%s, %s)"
		values = (self.organizerId, self.title)
		return UtilsBD.Instance().executeInsert(query,values)
			
		

	def toTuple(self):
		info = {"id" : self.id, "organizerId" : self.organizerId, "title" : self.title}
		return info
