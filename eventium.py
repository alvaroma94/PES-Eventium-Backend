from flask import Flask, Response, request
import sys
sys.path.append('./pruebasBD')
from connection import Connection
from gatewayTest import GatewayTest
from finderTest import FinderTest
import psycopg2



app = Flask(__name__)

connection = Connection.Instance()
connection.connect()

#si no existe la tabla la creo
try:
	cursor = connection.cursor()
	cursor.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
	print 'tabla test creada'
	connection.commit()
except psycopg2.ProgrammingError as err:
	print err
	cursor.close()
	connection.rollback()

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/tests", methods = ['GET'])
def getTests():
	finder = FinderTest.Instance()
	rows = finder.getAll()
	if (rows): # si no es nulo
		info = finder.tuplesToJson(rows)
		resp = Response(info, status=200, mimetype="application/json")
	else:
		resp = Response("Not found", status=404)
	return resp

@app.route("/test/<id>", methods = ['GET'])
def getTest(id):
	finder = FinderTest.Instance()
	row = finder.find(id)
	if (row):
		info = finder.tupleToJson(row)
		resp = Response(info, status=200, mimetype="application/json")	
	else:
		resp = Response("Not found", status=404)
	return resp

@app.route("/test", methods = ['POST'])
def postTest():
	id = request.form['id']
	num = request.form['num']
	data = request.form['data']
	newTest = GatewayTest(id,num,data)
	if (newTest.insert()): return "OK"
	else: return "ya existe"

if __name__ == "__main__":
	while True:
		try:
			app.run(use_reloader = False)
		except:
			pass
