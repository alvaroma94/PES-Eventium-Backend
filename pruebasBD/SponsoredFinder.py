import psycopg2
import SingletonPattern
from SponsoredGateway import SponsoredGateway
from connection import Connection
from utilsBD import UtilsBD
import json

@SingletonPattern.Singleton
class SponsoredFinder:
	def __init__(self):
		pass

	def checkIsSponsoring(self, sponsorId, eventId):
		query = "SELECT * FROM \"SPONSORED\" WHERE \"USERID\" = %s AND \"EVENTID\" = %s "
		values = (sponsorId,eventId)
		t = UtilsBD.Instance().executeSelect(query, values, fetchone = True)
		return t != None