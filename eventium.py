from flask import Flask, Response, request
import sys
sys.path.append('./pruebasBD')
from connection import Connection
from gatewayTest import GatewayTest
from finderTest import FinderTest
from UserGateway import UserGateway
from EventGateway import EventGateway
from EventFinder import EventFinder
from finderComment import FinderComment
from gatewayComment import GatewayComment
from utilsJSON import tupleToJson, tuplesToJson #pillo funciones
import psycopg2
import json



app = Flask(__name__)

connection = Connection.Instance()
connection.connect()

msgNotFound = json.dumps({ 'status' : 'Not found'})
msgCreatedOK = json.dumps({ 'status': 'Created'})
msgAlreadyExists = json.dumps({'status' : 'Already exists' })
msgDeletedOK = json.dumps({ 'status': 'Deleted'})
msgUpdatedOK = json.dumps({ 'status': 'Updated'})
msgTypeError = json.dumps({'status' : 'Type Error'})
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

@app.route("/event", methods = ['POST'])
def postEvent():
	id = request.form['id']
	organizerId = request.form['organizerId']
	title = request.form['title']
	newEvent = EventGateway(id,organizerId,title)
	error = newEvent.insert()
	if error == None:
		return Response(msgCreatedOK, status = 201, mimetype = "application/json")
	elif error == psycopg2.IntegrityError:
		return Response(msgAlreadyExists, status = 200, mimetype="application/json")
	elif error == psycopg2.DataError:
		return Response(msgTypeError, status = 400, mimetype="application/json")

@app.route("/event/<eventid>/comments", methods = ['GET'])
def getEventsComment(eventid):
	finder = FinderComment.Instance()
	rows = finder.findByEvent(id)
	if (rows):
		info = tuplesToJson(rows)
		return Response(info, status=200, mimetype="application/json")
	else:
		return Response(msgNotFound, status=404,  mimetype="application/json")

@app.route("/event/<eventid>/comment", methods = ['POST'])
def postEventComment(eventid):
	text = request.form['text']
	userid = request.form['userid']
	comment = GatewayComment(text = text, userid = userid, eventid = eventid)
	error = comment.insert()
	if error == None:
		return Response(msgCreatedOK, status = 201, mimetype = "application/json")
	elif error == psycopg2.IntegrityError:
		return Response(msgAlreadyExists, status = 200, mimetype="application/json")
	elif error == psycopg2.DataError:
		return Response(msgTypeError, status = 400, mimetype="application/json")

@app.route("/event", methods = ['GET'])
def getEventsTitle():
	titulo = request.headers['titulo']
	finder = EventFinder.Instance()
	rows = finder.getTitulo(titulo)
	if (rows): # si no es nulo
		info = tuplesToJson(rows) # rows tiene q ser un conjunto de gateways cualesquiera
		resp = Response(info, status=200, mimetype="application/json")
	else:
		resp = Response(msgNotFound, status=404,  mimetype="application/json")
	return resp

@app.route("/events", methods = ['GET'])
def getEvents():
	finder = EventFinder.Instance()
	rows = finder.getAll()
	if (rows): # si no es nulo
		info = tuplesToJson(rows) # rows tiene q ser un conjunto de gateways cualesquiera
		resp = Response(info, status=200, mimetype="application/json")
	else:
		resp = Response(msgNotFound, status=404,  mimetype="application/json")
	return resp

@app.route("/user", methods = ['POST'])
def postUser():
	id = request.form['id']
	username = request.form['username']
	password = request.form['password']
	mail = request.form['mail']
	newUser = UserGateway(id,username,password, mail)
	error = newUser.insert()
	if error == None:
		return Response(msgCreatedOK, status = 201, mimetype = "application/json")
	elif error == psycopg2.IntegrityError:
		return Response(msgAlreadyExists, status = 200, mimetype="application/json")
	elif error == psycopg2.DataError:
		return Response(msgTypeError, status = 400, mimetype="application/json")
	
@app.route("/")
def hello():
    return "Hello World!"

@app.route("/tests", methods = ['GET'])
def getTests():
	finder = FinderTest.Instance()
	rows = finder.getAll()
	if (rows): # si no es nulo
		info = tuplesToJson(rows) # rows tiene q ser un conjunto de gateways cualesquiera
		resp = Response(info, status=200, mimetype="application/json")
	else:
		resp = Response(msgNotFound, status=404,  mimetype="application/json")
	return resp

@app.route("/test/<id>", methods = ['GET'])
def getTest(id):
	finder = FinderTest.Instance()
	row = finder.find(id)
	if (row):
		info = tupleToJson(row) #row es un gateway cualquiera
		resp = Response(info, status=200, mimetype="application/json")	
	else:
		resp = Response(msgNotFound, status=404,  mimetype="application/json")
	return resp

@app.route("/test", methods = ['POST'])
def postTest():
	id = request.form['id']
	num = request.form['num']
	data = request.form['data']
	newTest = GatewayTest(id,num,data)
	error = newTest.insert()
	if error == None:
		return Response(msgCreatedOK, status = 201, mimetype = "application/json")
	elif error == psycopg2.IntegrityError:
		return Response(msgAlreadyExists, status = 200, mimetype="application/json")
	elif error == psycopg2.DataError:
		return Response(msgTypeError, status = 400, mimetype="application/json")


@app.route("/test", methods = ['DELETE'])
def deleteTest():
	print 'delete'
	id = request.form['id']
	print id
	finder = FinderTest.Instance()
	test = finder.find(id)
	print test
	if (test):
		print 'lo voy a borrar'
		test.remove()
		return Response(msgDeletedOK, status = 201, mimetype = "application/json")
	else:
		return Response(msgNotFound, status=404,  mimetype="application/json")

@app.route("/test", methods = ['PUT'])
def updateTest():
	id = request.form['id']
	finder = FinderTest.Instance()
	test = finder.find(id)
	if(test):
		num = request.form['num']
		data = request.form['data']
		test.num = num
		test.data = data
		error = test.update()
		if error == None: 
			return Response(msgUpdatedOK, status = 201, mimetype = "application/json")
		elif error == psycopg2.DataError:
			return Response(msgTypeError, status = 400, mimetype = "application/json")
	else:
		return Response(msgNotFound, status=404,  mimetype="application/json")

if __name__ == "__main__":
	while True:
		try:
			app.run(use_reloader = False, debug = True)
		except:
			pass
