import psycopg2
from connection import Connection
import json



class Event:
	def __init__(self, id, organizerId):
		self.id = id
		self.organizerId = organizerId

	def insert(self):
		ret = True
		try:
			c = Connection.Instance()
			cursor = c.cursor()
			query = "INSERT INTO event (id, organizerid) VALUES (%s ,%s)"
			values = (self.id, self.organizerId)
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
		query = "DELETE FROM event WHERE id = %s"
		values = (self.id,)
		cursor.execute(query, values)
		c.commit()
		cursor.close()