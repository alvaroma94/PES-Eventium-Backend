import psycopg2
import SingletonPattern
from CategoriesGateway import CategoriesGateway
from connection import Connection
from utilsBD import UtilsBD
import json

#patron finder de Row Data Gateway
@SingletonPattern.Singleton
class CategoriesFinder:
	def __init__(self):
		pass

	def findById(self, id):
		query = "SELECT \"CATEGORYID\" FROM \"LIKINGS\" WHERE \"USERID\" = %s"
		values = (id,)
		t = UtilsBD.Instance().executeSelect(query, values, fetchone = False)
		categories = []
		if t: categories = [int(c[0]) for c in t]
		return CategoriesGateway(id = id, categories = categories)