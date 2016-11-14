from flask import Flask, Response, request
import sys
import psycopg2
sys.path.append('./pruebasBD')
from utilsBD import UtilsBD
from connection import Connection
from utilsJSON import tupleToJson, tuplesToJson #pillo funciones
import json

#en el server se haria
c = Connection.Instance().connect()

# Open a file
fo = open("./Schema/Declarations.txt", "r")
input = fo.read();
#print "Read String is : ", str
# Close opend file
fo.close()
c = Connection.Instance()
cursor = c.cursor()
try:
	cursor.execute("DROP SCHEMA public CASCADE;")
	c.commit()
except Exception, e:
	Connection.Instance().rollback()
	
try:
	cursor.execute("CREATE SCHEMA public;")
	c.commit()
except Exception, e:
	Connection.Instance().rollback()

# all SQL commands (split on ';')
sqlCommands = input.split(';')
print sqlCommands
for command in sqlCommands[1:-1]:
	print command
	try:
		cursor.execute(command)
		c.commit()
	except Exception, e:
		print e
		Connection.Instance().rollback()

categories = json.dumps({'1' : 'artistico', '2' : 'automobilistico', '3' : 'cinematografico', '4' : 'deportivo', '5': 'literario', '6':'moda', '7':'musical', '8':'otros', '9': 'politico', '10':'teatral', '11':'tecnologico_y_cientifico'})
categories = json.loads(categories)
for x in range(1, 12):
	print categories[str(x)]
	try:
		cursor.execute("INSERT INTO \"CATEGORY\" (\"NAME\") VALUES ('"+categories[str(x)]+"');")
		#postgres treats " as a way to define identifiers and ' as a way to define strings ^
		c.commit()
	except Exception, e:
		print e
		Connection.Instance().rollback()
	
cursor.close()
