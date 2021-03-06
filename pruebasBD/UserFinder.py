import psycopg2
import SingletonPattern
from UserGateway import UserGateway
from connection import Connection
from utilsBD import UtilsBD
import json

def getValoration(id):
	query = "SELECT AVG(\"POINTS\") FROM \"VALORATION\" c, \"EVENT\" e WHERE c.\"EVENTID\" = e.\"ID\" and e.\"ORGANIZERID\" = %s"
	values = (id,)
	average = UtilsBD.Instance().executeSelect(query, values, fetchone = True)
	if (average[0] != None):
		 return average[0]
	else:
		 return ""
def perteneceRango(id,estrellasMin, estrellasMax):

	if not estrellasMin and not estrellasMax:
		return True

	valoration = getValoration(id)
	if valoration == "": valoration = 0

	if estrellasMin and estrellasMax:
		return float(valoration) >= float(estrellasMin) and float(valoration) <= float(estrellasMax)
	elif estrellasMin:
		return float(valoration) >= float(estrellasMin)
	else: 
		return float(valoration) <= float(estrellasMax)

#patron finder de Row Data Gateway
@SingletonPattern.Singleton
class UserFinder:
	def __init__(self):
		pass

	def findForDeposit(self, id):
		query = "SELECT \"SALDO\" FROM \"USER\" WHERE \"ID\" = %s AND \"SPONSOR\" = false "
		values = (id,)
		t = UtilsBD.Instance().executeSelect(query, values, fetchone = True)
		if (t):
			print t
			user = UserGateway(id = id, username = None, password = None, mail = None, wallet = t[0])
			return user
		return t

	def findByName(self, username):
		query = "SELECT * FROM \"USER\" WHERE \"USERNAME\" = %s ORDER BY \"USERNAME\""
		values = (username,)
		t = UtilsBD.Instance().executeSelect(query, values, fetchone = True)
		if (t):
			user = UserGateway(id = t[0], username = t[1], password = t[2], mail = t[3], pic = t[6], wallet = t[5], verified = t[7], valoration = getValoration(t[0]), ciudad = t[10], nreports = t[11])
			return user
		return t

	def getAll(self):
		query = "SELECT * FROM \"USER\" WHERE \"SPONSOR\" = false ORDER BY \"USERNAME\""
		tuples = UtilsBD.Instance().executeSelect(query, None, fetchone = False)
		ret = []
		for t in tuples:
			test = UserGateway(id = t[0], username = t[1], password = t[2], mail = t[3], pic = t[6], wallet = t[5], verified = t[7], banned = t[8], valoration = getValoration(t[0]), ciudad = t[10], nreports = t[11])
			ret.append(test)
		return ret


	def getAll(self,estrellasMin,estrellasMax,ciudad):
		query = "SELECT * FROM \"USER\" WHERE \"SPONSOR\" = false"
		if ciudad:
			query = query + " AND \"CIUDAD\" ILIKE '%s' " % (ciudad)
		query = query + " ORDER BY \"USERNAME\""
		tuples = UtilsBD.Instance().executeSelect(query, None, fetchone = False)
		ret = []
		for t in tuples:
			if perteneceRango(t[0],estrellasMin, estrellasMax):
				test = UserGateway(id = t[0], username = t[1], password = t[2], mail = t[3], pic = t[6], wallet = t[5], verified = t[7], banned = t[8], valoration = getValoration(t[0]), ciudad = t[10], nreports = t[11])
				ret.append(test)
		return ret

	
	def findByMailOrUser(self, clave):

		query = "SELECT * FROM \"USER\" WHERE  \"SPONSOR\" = false AND (\"USERNAME\" = %s or  \"MAIL\" = %s)"
		values = (clave, clave)
		t = UtilsBD.Instance().executeSelect(query, values, fetchone = True)
		if (t):
			user = UserGateway(id = t[0], username = t[1], password = t[2], mail = t[3], pic = t[6], wallet = t[5], verified = t[7], valoration = getValoration(t[0]), ciudad = t[10], nreports = t[11])
			return user
		return t

	def findForLogin(self, username, password):
		query = "SELECT * FROM \"USER\" WHERE \"USERNAME\" = %s and  \"PASSWORD\" = %s"
		values = (username, password)
		t = UtilsBD.Instance().executeSelect(query, values, fetchone = True)
		if (t):
			user = UserGateway(id = t[0], username = t[1], password =None, mail = t[3], pic = t[6], ciudad = t[10], nreports = t[11], banned = t[8])
			return user
		return t

	def findById(self, id):
		query = "SELECT * FROM \"USER\" WHERE \"ID\" = %s"
		values = (id,)
		t = UtilsBD.Instance().executeSelect(query, values, fetchone = True)
		if (t):
			print 'nreports', t[11]
			print 'sponsor', t[9]
			user = UserGateway(id = t[0], username = t[1], password =t[2], mail = t[3], pic = t[6], verified = t[7],  banned = t[8], valoration = getValoration(t[0]), ciudad = t[10], sponsor = t[9], nreports = t[11])
			return user
		return t

	def findSponsors(self):
		query = "SELECT * FROM \"USER\" WHERE \"SPONSOR\" = true ORDER BY \"USERNAME\""
		tuples = UtilsBD.Instance().executeSelect(query, None, fetchone = False)
		ret = []
		for t in tuples:
			test = UserGateway(id = t[0], username = t[1], mail = t[3], pic = t[6])
			ret.append(test)
		return ret