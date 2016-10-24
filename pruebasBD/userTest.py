import psycopg2
from connection import Connection
import json
from utilsBD import UtilsBD

#patron row data gateway (cada instancia de la clase es una fila de la bd)
class UserGateway:
	def __init__(self, id, username, password, mail):
		#variables privadas de la clase
		self.id = id
		self.username = username
		self.password = password
		self.mail = mail

	def insert(self):
		query = "INSERT INTO USER (ID, USERNAME, PASSWORD) VALUES (%s ,%s, %s)"
		values = (self.id, self.username, self.password)
		return UtilsBD.Instance().executeInsert(query,values)
					

	def toTuple(self):
		info = {"id" : self.id, "username" : self.username, "password" : self.password, "mail" : self.mail}
		return info


