import psycopg2
from connection import Connection
import json
from utilsBD import UtilsBD

#patron row data gateway (cada instancia de la clase es una fila de la bd)
class EventGateway:
	def __init__(self, id ="", organizerId ="", title ="", horaf ="", horai ="",fechaf ="",fechai ="",precio="",pic ="",ciudad="",categoria="", destacado = False, descripcion = "", url = "", nreports = 0):
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
		self.destacado = destacado
		self.descripcion = descripcion
		self.url = url
		self.nreports = nreports

	def insert(self):
		query = "INSERT INTO \"EVENT\" (\"ORGANIZERID\", \"TITLE\", \"FECHA_FIN\", \"FECHA_INI\", \"HORA_FIN\", \"HORA_INI\", \"PRECIO\", \"PIC\", \"CIUDAD\", \"CATEGORIA\", \"DESTACADO\", \"DESCRIPCION\",\"URL\",\"NREPORTS\") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		values = (self.organizerId, self.title, self.fechaf, self.fechai, self.horaf, self.horai, self.precio, self.pic, self.ciudad, self.categoria, self.destacado, self.descripcion, self.url,self.nreports)
		return UtilsBD.Instance().executeInsert(query,values)
	def update(self):
		query = "UPDATE \"EVENT\"  SET \"TITLE\" = %s, \"FECHA_INI\" = %s, \"FECHA_FIN\" = %s, \"HORA_INI\" = %s, \"HORA_FIN\" = %s, \"PRECIO\" = %s, \"PIC\" = %s, \"CIUDAD\" = %s, \"CATEGORIA\" = %s ,  \"DESTACADO\" = %s, \"DESCRIPCION\" = %s, \"URL\" = %s, \"NREPORTS\" = %s WHERE \"ID\" = %s"
		values = (self.title, self.fechai, self.fechaf, self.horai, self.horaf, self.precio, self.pic, self.ciudad, self.categoria, self.destacado, self.descripcion, self.url, self.nreports,self.id)
		return UtilsBD.Instance().executeUpdate(query,values)
	def toTuple(self):
		info = {"id" : self.id, "organizerId" : self.organizerId, "title" : self.title , "fecha_ini" : self.fechai, "fecha_fin" : self.fechaf, "hora_ini" : self.horai, "hora_fin" : self.horaf, "precio" : self.precio, "pic" : self.pic, "ciudad" : self.ciudad, "categoria": self.categoria, "destacado":self.destacado, "descripcion":self.descripcion, "url": self.url, "nreports": self.nreports}
		return info

	def delete(self):
		query = "DELETE FROM \"EVENT\" WHERE \"ID\" = %s"
		values = (self.id,)
		UtilsBD.Instance().executeRemove(query,values)