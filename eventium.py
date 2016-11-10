from flask import Flask, Response, request
import sys
sys.path.append('./pruebasBD')
from flask_mail import Mail
from flask_mail import Message
from connection import Connection
from gatewayTest import GatewayTest
from finderTest import FinderTest
from UserGateway import UserGateway
from UserFinder import UserFinder
from EventGateway import EventGateway
from EventFinder import EventFinder
from finderComment import FinderComment
from gatewayComment import GatewayComment
from gatewayValoration import GatewayValoration
from gatewayFollowing import GatewayFollowing
from finderFollowing import FinderFollowing
from utilsJSON import tupleToJson, tuplesToJson #pillo funciones
import psycopg2
import json



app = Flask(__name__)
mail = Mail(app)
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'eventiumbcn@gmail.com',
	MAIL_PASSWORD = 'eventium321'
	)
mail = Mail(app)

connection = Connection.Instance()
connection.connect()

msgNotFound = json.dumps({ 'status' : 'Not found'})
msgCreatedOK = json.dumps({ 'status': 'Created'})
msgAlreadyExists = json.dumps({'status' : 'Already exists' })
msgDeletedOK = json.dumps({ 'status': 'Deleted'})
msgUpdatedOK = json.dumps({ 'status': 'Updated'})
msgTypeError = json.dumps({'status' : 'Type Error'})
msgGoodMail= json.dumps({'status' : 'La password ha sido enviada a tu mail'})
msgBadMail= json.dumps({'status' : 'El usuario o mail no existe'})
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
@app.route("/mail", methods = ['GET'])
def sendMail():
	clave = request.headers['clave']
	finder = UserFinder.Instance()
	row = finder.findByMailOrUser(clave)
	if (row):
		#info = tupleToJson(row) #row es un gateway cualquiera
		username = row.getUsername()
		password =  row.getPassword()
		maill = row.getMail()
		msg = Message("Password", sender="admin@eventium.com", recipients=[maill])
		msg.body = "Hola " + username + " tu password es la siguiente: " + password
		mail.send(msg)
		return Response(msgGoodMail, status=200, mimetype="application/json")	
	else:
		return Response(msgBadMail, status=404,  mimetype="application/json")
	

@app.route("/event", methods = ['POST'])
def postEvent():

	id = request.form['id']
	organizerId = request.form['organizerId']
	title = request.form['title']
	horaf = request.form['hora_fin']
	horai = request.form['hora_ini']
	fechaf = request.form['fecha_fin']
	fechai = request.form['fecha_ini']
	precio = request.form['precio']
	pic = request.form['pic']
	ciudad = request.form['ciudad']
	print 'oly'
	newEvent = EventGateway(id,organizerId,title, horaf, horai , fechaf, fechai, precio, pic, ciudad)
	error = newEvent.insert()
	if error == None:
		return Response(msgCreatedOK, status = 201, mimetype = "application/json")
	elif error == psycopg2.IntegrityError:
		return Response(msgAlreadyExists, status = 200, mimetype="application/json")
	elif error == psycopg2.DataError:
		return Response(msgTypeError, status = 400, mimetype="application/json")

@app.route("/events/<eventid>/comments", methods = ['GET'])
def getEventsComment(eventid):
	finder = FinderComment.Instance()
	rows = finder.findByEvent(eventid)
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

@app.route("/events/<eventid>/valoration", methods = ['POST'])
def postEventValoration(eventid):
	points = request.form['points']
	userid = request.form['userid']
	valoration = GatewayValoration(points = points, userid = userid, eventid = eventid)
	error = valoration.insert()
	if error == None:
		return Response(msgCreatedOK, status = 201, mimetype = "application/json")
	elif error == psycopg2.IntegrityError:
		return Response(msgAlreadyExists, status = 200, mimetype="application/json")
	elif error == psycopg2.DataError:
		return Response(msgTypeError, status = 400, mimetype="application/json")

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

@app.route("/users", methods = ['GET'])
def getUsers():
	finder = UserFinder.Instance()
	rows = finder.getAll()
	if (rows): # si no es nulo
		info = tuplesToJson(rows) # rows tiene q ser un conjunto de gateways cualesquiera
		resp = Response(info, status=200, mimetype="application/json")
	else:
		resp = Response(msgNotFound, status=404,  mimetype="application/json")
	return resp

@app.route("/user", methods = ['POST'])
def postUser():
	username = request.form['username']
	password = request.form['password']
	mail = request.form['mail']
	pic = request.form['pic']
	newUser = UserGateway(None, username, password, mail, pic)
	error = newUser.insert()
	if error == None:
		return Response(msgCreatedOK, status = 201, mimetype = "application/json")
	elif error == psycopg2.IntegrityError:
		return Response(msgAlreadyExists, status = 200, mimetype="application/json")
	elif error == psycopg2.DataError:
		return Response(msgTypeError, status = 400, mimetype="application/json")

@app.route("/users/<name>", methods = ['GET'])
def getUser(name):
	finder = UserFinder.Instance()
	row = finder.findByName(name)
	if (row):
		info = tupleToJson(row) #row es un gateway cualquiera
		return Response(info, status=200, mimetype="application/json")
	else:
		return Response(msgNotFound, status=404,  mimetype="application/json")		

@app.route("/user/<id>/follows", methods = ['GET'])
def getUserFollows(id):
	rows = FinderFollowing.Instance().find(id)
	if (rows): # si no es nulo
		info = tuplesToJson(rows) # rows tiene q ser un conjunto de gateways cualesquiera
		resp = Response(info, status=200, mimetype="application/json")
	else:
		resp = Response(msgNotFound, status=404,  mimetype="application/json")
	return resp

@app.route("/user/<id>/follows", methods = ['POST'])
def postUserFollows(id):
	followedId = request.form['followed']
	newFollows = GatewayFollowing(id, followedId)
	error = newFollows.insert()
	if error == None:
		return Response(msgCreatedOK, status = 201, mimetype = "application/json")
	elif error == psycopg2.IntegrityError:
		return Response(msgAlreadyExists, status = 200, mimetype="application/json")
	elif error == psycopg2.DataError:
		return Response(msgTypeError, status = 400, mimetype="application/json")

@app.route("/user/<id>/follows/<followed>", methods = ['DELETE'])
def deleteUserFollows(id, followed):
	follows = GatewayFollowing(id, followed)
	error = follows.remove()
	if error == None:
		return Response(msgDeletedOK, status = 201, mimetype = "application/json")
	else:
		return Response(msgNotFound, status=404,  mimetype="application/json")

@app.route("/user/<id>/subscription/<followed>", methods = ['PUT'])
def putUserSubscription(id, followed):
	subscribed = request.form['subscribed']
	finder = FinderFollowing.Instance()
	follows = finder.findSubscription(id,followed)
	follows.subscribed = subscribed == "True"
	error = follows.update()
	if error == None:
		return Response(msgUpdatedOK, status=200, mimetype="application/json")
	else:
		return Response(msgNotFound, status=404,  mimetype="application/json")

@app.route("/user/<id>/wallet", methods = ['PUT'])
def putUserWallet(id):
	cardNumber = request.form['card']
	cvc = request.form['cvc']
	money = request.form['money']
	
	user = UserFinder.Instance().findForDeposit(id)

	# esto es provisional
	if user.wallet: user.wallet += int(money)
	else: user.wallet = int(money)

	user.updateWallet()

	return Response(msgUpdatedOK, status=200, mimetype="application/json")

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
