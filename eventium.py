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
from CategoriesGateway import CategoriesGateway
from CategoriesFinder import CategoriesFinder
from utilsJSON import tupleToJson, tuplesToJson #pillo funciones
import psycopg2
import json

#esto es para el token
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)



app = Flask(__name__)
app.config['SECRET_KEY'] = 'holaquetal'
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

msgNotFound = json.dumps({'code' : 404, 'status' : 'Not found'})
msgNoPermission = json.dumps({ 'code' : 401, 'status' : 'No permission'})
msgCreatedOK = json.dumps({ 'code' : 201, 'status': 'Created'})
msgAlreadyExists = json.dumps({ 'code' : 200, 'status' : 'Already exists' })
msgDeletedOK = json.dumps({ 'status': 'Deleted'})
msgUpdatedOK = json.dumps({ 'code' : 200, 'status': 'Updated'})
msgTypeError = json.dumps({'code' : 400, 'status' : 'Type Error'})
msgGoodMail= json.dumps({'code' : 200, 'status' : 'La password ha sido enviada a tu mail'})
msgBadMail= json.dumps({'code' : 404, 'status' : 'El usuario o mail no existe'})

categories = json.dumps({'1' : 'artistico', '2' : 'automobilistico', '3' : 'cinematografico', '4' : 'deportivo', '5': 'literario', '6':'moda', '7':'musical', '8':'otros', '9': 'politico', '10':'teatral', '11':'tecnologico_y_cientifico'})
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

# https://blog.miguelgrinberg.com/post/restful-authentication-with-flask
def generate_auth_token(mid):
    s = Serializer(app.config['SECRET_KEY'])
    token = s.dumps({'id': mid})
    return token

def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
    	print 'signature expired'
        return False # valid token, but expired
    except BadSignature:
    	print 'bad signature'
        return False # invalid token
	id = data['id']
	finder = UserFinder.Instance()
	row = finder.findById(id)
	if not row: return False
    else: return data['id']#devuelve el id asociado a ese token

@app.route("/categories", methods = ['GET'])
def getCategories():
	return Response(categories, status=200,  mimetype="application/json")

#Pending
@app.route("/login", methods = ['POST'])
def login():
	username = request.form['username']
	password = request.form['password']
	finder = UserFinder.Instance()
	row = finder.findForLogin(username,password)
	if (row):
		mid = row.id
		print 'la id es ', mid
		info = tupleToJson(row)
		infoToken = {'token' : generate_auth_token(mid)}
		print 'info token', infoToken
		aux = json.dumps(infoToken)
		return Response(json.dumps(aux,info), status=200,  mimetype="application/json")
	return Response(msgNotFound, status=404,  mimetype="application/json")

#Pending
@app.route("/users/<id>/perfil", methods = ['GET'])
def getPerfilUser(id):
	token = request.headers['token']
	idCorresponiente = verify_auth_token(token)
	print 'id corresponde a' , idCorresponiente, 'mi id es', id
	if int(idCorresponiente) == int(id):
		return Response(json.dumps({'id':id}), status=200,  mimetype="application/json")
	else: return Response(msgNoPermission, status=401,  mimetype="application/json")


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
	
#Pending
#Id is serial no hay que pasarla como parametro
#deberia guardarse como datetime las fechas
#-https://www.postgresql.org/docs/9.1/static/datatype-datetime.html
@app.route("/events", methods = ['POST'])
def postEvent():
	token = request.headers['token']
	organizerId = verify_auth_token(token)
	if not organizerId: return Response(msgNoPermission, status=401,  mimetype="application/json")
	title = request.form['title']
	horaf = request.form['hora_fin']
	horai = request.form['hora_ini']
	fechaf = request.form['fecha_fin']
	fechai = request.form['fecha_ini']
	precio = request.form['precio']
	pic = request.form['pic']
	ciudad = request.form['ciudad']
	categoria = request.form['categoria']
	newEvent = EventGateway("", organizerId, title, horaf, horai , fechaf, fechai, precio, pic, ciudad, categoria)
	error = newEvent.insert()
	if error == None:
		return Response(msgCreatedOK, status = 201, mimetype = "application/json")
	elif error == psycopg2.IntegrityError:
		return Response(msgAlreadyExists, status = 200, mimetype="application/json")
	elif error == psycopg2.DataError:
		return Response(msgTypeError, status = 400, mimetype="application/json")

#Pending
@app.route("/events/<eventid>/comments", methods = ['GET'])
def getEventsComment(eventid):
	finder = FinderComment.Instance()
	rows = finder.findByEvent(eventid)
	if (rows):
		info = tuplesToJson(rows)
		return Response(info, status=200, mimetype="application/json")
	else:
		return Response(msgNotFound, status=404,  mimetype="application/json")
#Pending
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
#Pending
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
#Pending
@app.route("/events", methods = ['GET'])
def getEvents():

	fecha_ini = request.args.get('fecha_ini')
	fecha_fin = request.args.get('fecha_fin')
	hora_ini = request.args.get('hora_ini')
	hora_fin = request.args.get('hora_fin')
	titulo = request.args.get('titulo')
	precio = request.args.get('precio')
	ciudad = request.args.get('ciudad')

	finder = EventFinder.Instance()
	rows = finder.getAll(fecha_ini, fecha_fin, hora_ini, hora_fin, titulo, precio, ciudad)
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

@app.route("/users", methods = ['POST'])
def postUser():
	username = request.form['username']
	password = request.form['password']
	mail = request.form['mail']
	pic = request.form['pic']
	saldo = request.form['saldo']
	newUser = UserGateway(None, username, password, mail, pic,saldo)
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
#Pending
@app.route("/user/<id>/follows", methods = ['GET'])
def getUserFollows(id):
	rows = FinderFollowing.Instance().find(id)
	if (rows): # si no es nulo
		info = tuplesToJson(rows) # rows tiene q ser un conjunto de gateways cualesquiera
		resp = Response(info, status=200, mimetype="application/json")
	else:
		resp = Response(msgNotFound, status=404,  mimetype="application/json")
	return resp
#Pending
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
#Pending
@app.route("/user/<id>/follows/<followed>", methods = ['DELETE'])
def deleteUserFollows(id, followed):
	follows = GatewayFollowing(id, followed)
	error = follows.remove()
	if error == None:
		return Response(msgDeletedOK, status = 201, mimetype = "application/json")
	else:
		return Response(msgNotFound, status=404,  mimetype="application/json")
#Pending
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
#Pending
#Algun error al hacer la query
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
	
#Pending
#se podria pasar el true/false por la url
#algun error con la query
@app.route("/users/<id>/verified", methods = ['PUT'])
def putUserVerified(id):
	isVerified = request.form['verified']
	user = UserFinder.Instance().findById(id)
	user.verified = isVerified
	error = user.update()
	if error == None:
		return Response(msgUpdatedOK, status=200, mimetype="application/json")
	else:
		return Response(msgNotFound, status=404,  mimetype="application/json")


@app.route("/users/<id>/categories", methods = ['PUT'])
def setUserCategories(id):
	categories = request.form['categories']
	# formato en el form : 1,2,3,4
	categories.encode('ascii', 'ignore')
	l = []
	if (categories != ""):
		l = categories.split(',')
		l = [int(i) for i in l] # lo paso a enteros
	CategoriesGateway(int(id), l).update()
	return Response(msgUpdatedOK,status=200, mimetype="application/json")
	
#Igual quitar el id de la respuesta? ya lo tienen a la hora de enviar
@app.route("/users/<id>/categories", methods = ['GET'])
def getUserCategories(id):
	row = CategoriesFinder.Instance().findById(int(id))
	result = tupleToJson(row)
	return Response(result, status=200, mimetype="application/json")
	
if __name__ == "__main__":
	while True:
		try:
			app.run(use_reloader = False, debug = True)
		except:
			pass
