import psycopg2
from connection import Connection
import json
from utilsBD import UtilsBD

#patron row data gateway (cada instancia de la clase es una fila de la bd)
class EventGateway:
	def __init__(self, id, organizerId, title, horaf, horai,fechaf,fechai,precio,pic,ciudad,categoria):
		#variables privadas de la clase
		self.id = id
		self.organizerId = organizerId
		self.title = title
		self.horaf = horaf
		self.horai = horai
		self.fechaf = fechaf
		self.fechai = fechai
		self.precio = precio
		self.pic = pic
		self.ciudad = ciudad
		self.categoria = categoria

	def insert(self):
		
		query = "INSERT INTO \"EVENT\" (\"ORGANIZERID\", \"TITLE\", \"FECHA_FIN\", \"FECHA_INI\", \"HORA_FIN\", \"HORA_INI\", \"PRECIO\", \"PIC\", \"CIUDAD\", \"CATEGORIA\") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		values = (self.organizerId, self.title, self.fechaf, self.fechai, self.horaf, self.horai, self.precio, self.pic, self.ciudad, self.categoria)
		return UtilsBD.Instance().executeInsert(query,values)

	def toTuple(self):
		info = {"id" : self.id, "organizerId" : self.organizerId, "title" : self.title , "fecha_ini" : self.fechai, "fecha_fin" : self.fechaf, "hora_ini" : self.horai, "hora_fin" : self.horaf, "precio" : self.precio, "pic" : self.pic, "ciudad" : self.ciudad, "categoria": self.categoria}
		return info
