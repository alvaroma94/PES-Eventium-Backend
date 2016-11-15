import psycopg2
from connection import Connection
import json
from utilsBD import UtilsBD

#patron row data gateway (cada instancia de la clase es una fila de la bd)
class UserGateway:
	def __init__(self, id, username = "", password = "", mail = "", pic = "" , wallet = 0 , verified = False):
		#variables privadas de la clase
		self.id = id
		self.username = username
		self.password = password
		self.mail = mail
		self.pic = pic
		self.wallet = wallet
		self.verified = verified
	def getPassword(self):    
		return self.password
	def getMail(self):
		return self.mail
	def getUsername(self):
		return self.username

	def insert(self):
		query = "INSERT INTO \"USER\"   (\"USERNAME\" , \"PASSWORD\" , \"MAIL\", \"PIC\", \"VERIFIED\", \"SALDO\" ) VALUES (%s, %s, %s, %s, %s, %s)"
		values = (self.username, self.password, self.mail, self.pic, self.verified, self.wallet)
		return UtilsBD.Instance().executeInsert(query,values)

	def update(self):
		query = "UPDATE \"USER\"  SET \"VERIFIED\" = %s WHERE \"ID\" = %s"
		values = (self.verified, self.id)
		return UtilsBD.Instance().executeUpdate(query,values)
					
	def updateWallet(self):
		query = "UPDATE \"USER\" SET \"SALDO\" = %s WHERE \"ID\" = %s"
		values = (self.wallet, self.id)
		return UtilsBD.Instance().executeInsert(query,values)

	def toTuple(self):
		info = {"id" : self.id, "username" : self.username, "password" : self.password, "mail" : self.mail, "pic":self.pic, "saldo" : self.wallet, "verified":self.verified}
		return info

	def toWallet(self):
		info = {"id": self.id, "wallet": self.wallet}

