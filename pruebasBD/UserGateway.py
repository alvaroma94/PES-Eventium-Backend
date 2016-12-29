import psycopg2
from connection import Connection
import json
from utilsBD import UtilsBD

#patron row data gateway (cada instancia de la clase es una fila de la bd)
class UserGateway:
	def __init__(self, id, username = "", password = "", mail = "", pic = "" , wallet = 0 , verified = False,  banned = False, ciudad = "", valoration= "", sponsor = False, nreports = 0):
		#variables privadas de la clase
		self.id = id
		self.username = username
		self.password = password
		self.mail = mail
		self.pic = pic
		self.wallet = wallet
		self.verified = verified
		self.banned = banned
		self.valoration = valoration
		self.ciudad = ciudad
		self.sponsor = sponsor
		self.nreports = nreports


	def getPassword(self):    
		return self.password
	def getMail(self):
		return self.mail
	def getUsername(self):
		return self.username

	def insert(self):
		query = "INSERT INTO \"USER\"   (\"USERNAME\" , \"PASSWORD\" , \"MAIL\", \"PIC\", \"VERIFIED\", \"SALDO\", \"CIUDAD\", \"NREPORTS\" ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
		values = (self.username, self.password, self.mail, self.pic, self.verified, self.wallet, self.ciudad,self.nreports)
		return UtilsBD.Instance().executeInsert(query,values)

	def update(self):
		query = "UPDATE \"USER\"  SET \"VERIFIED\" = %s, \"PASSWORD\" = %s, \"PIC\" = %s, \"BANNED\" = %s , \"CIUDAD\" = %s WHERE \"ID\" = %s"
		values = (self.verified, self.password, self.pic, self.banned, self.ciudad, self.id)
		return UtilsBD.Instance().executeUpdate(query,values)
					
	def updateWallet(self):
		query = "UPDATE \"USER\" SET \"SALDO\" = %s WHERE \"ID\" = %s"
		values = (self.wallet, self.id)
		return UtilsBD.Instance().executeInsert(query,values)

	def updateReports(self):
		query = "UPDATE \"USER\" SET \"NREPORTS\" = %s WHERE \"ID\" = %s"
		values = (self.nreports, self.id)
		return UtilsBD.Instance().executeInsert(query,values)

	def updateBanned(self):
		query = "UPDATE \"USER\" SET \"BANNED\" = %s WHERE \"ID\" = %s"
		values = (self.banned, self.id)
		return UtilsBD.Instance().executeInsert(query,values)

	def delete(self):
		query = "DELETE FROM \"USER\" WHERE \"ID\" = %s"
		values = (self.id,)
		UtilsBD.Instance().executeRemove(query,values)

	def toTuple(self):
		info = {"id" : self.id, "username" : self.username, "password" : self.password, "mail" : self.mail, "pic":self.pic, "saldo" : self.wallet, "verified":self.verified, "banned":self.banned, "valoration":str(self.valoration), "ciudad":self.ciudad, "nreports":self.nreports}
		return info

	def toWallet(self):
		info = {"id": self.id, "wallet": self.wallet}

