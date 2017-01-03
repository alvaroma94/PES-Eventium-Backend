import psycopg2
from connection import Connection
import SingletonPattern


def defaultQuery(query,values): # esta funcion esta fuera de la clase
	c = Connection.Instance()
	cursor = c.cursor()
	cursor.execute(query, values)
	c.commit()
	cursor.close()

@SingletonPattern.Singleton
class UtilsBD: 
	def __init__(self):
		pass
	def executeInsert(self, query, values):
		err = None
		try:
			defaultQuery(query, values)
		except psycopg2.IntegrityError as exc:
			print exc
			err = psycopg2.IntegrityError
			Connection.Instance().rollback()
		except psycopg2.DataError as exc:
			print exc
			err = psycopg2.DataError
			Connection.Instance().rollback()
		return err
		
	def executeSelect(self, query, values, fetchone):
		c = Connection.Instance()
		cursor = c.cursor()
		if (values != None): cursor.execute(query, values)
		else: cursor.execute(query)
		if fetchone:
			tuples = cursor.fetchone() #devuelve una lista de tuplas
		else:
			tuples = cursor.fetchall() #deuvuelve una sola tupla (no una lista)
		return tuples

	def executeRemove(self, query, values):
		err = None
		try:
			defaultQuery(query, values)
		except:
			err = True
			Connection.Instance().rollback()
		return err

	def executeUpdate(self, query, values):
		err = None
		try:
			defaultQuery(query, values)
		except psycopg2.DataError as exc:
			print exc
			err = psycopg2.DataError
			Connection.Instance().rollback()
		return err