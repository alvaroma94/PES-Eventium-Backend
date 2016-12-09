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
from CalendarGateway import CalendarGateway
from CalendarFinder import CalendarFinder
from gatewayComment import GatewayComment
from gatewayValoration import GatewayValoration
from gatewayFollowing import GatewayFollowing
from finderFollowing import FinderFollowing
from CategoriesGateway import CategoriesGateway
from CategoriesFinder import CategoriesFinder
from SponsoredGateway import SponsoredGateway
from utilsJSON import tupleToJson, tuplesToJson #pillo funciones
import psycopg2
import json
from datetime import date

#esto es para el token
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)



app = Flask(__name__)
app.config['SECRET_KEY'] = 'holaquetal'
mail = Mail(app)
'''
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'eventiumbcn@gmail.com',
	MAIL_PASSWORD = 'eventium321'
	)
'''
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'eventium666@gmail.com',
	MAIL_PASSWORD = '666eventiu'
	)

mail = Mail(app)

connection = Connection.Instance()
connection.connect()

msgNotFound = json.dumps({'status' : 'Not found'})
msgNoPermission = json.dumps({'status' : 'No permission'})
msgCreatedOK = json.dumps({'status': 'Created'})
msgAlreadyExists = json.dumps({ 'status' : 'Already exists' })
msgDeletedOK = json.dumps({ 'status': 'Deleted'})
msgUpdatedOK = json.dumps({'status': 'Updated'})
msgTypeError = json.dumps({'status' : 'Type Error'})
msgGoodMail= json.dumps({'status' : 'La password ha sido enviada a tu mail'})
msgBadMail= json.dumps({'status' : 'El usuario o mail no existe'})
msgForbiddenAction = json.dumps({'status' : 'Operacion no permitida'})
msgEmailSent = json.dumps({'status' : 'Mail enviado'})

categories = json.dumps({'0' : 'artistico', '1' : 'automobilistico', '2' : 'cinematografico', '3' : 'deportivo', '4' : 'gastronomico' , '5': 'literario', '6':'moda', '7':'musical', '8':'otros', '9': 'politico', '10':'teatral', '11':'tecnologico_y_cientifico'})
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
def generate_sponsor_token(mid,eventid):
	s = Serializer(app.config['SECRET_KEY'])
	token = s.dumps({'id': mid, 'eventid':eventid})
	return token

def verify_sponsor_token(token):
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
	eventid = data['eventid']
	return (id, eventid)

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

#pending to document now returns name too
@app.route("/me", methods = ['GET'])
def me():
	id = verify_auth_token(request.headers['token'])
	if (not id): return Response(msgNotFound, status=404,  mimetype="application/json")
	user = UserFinder.Instance().findById(int(id))
	msg = {'username':user.username}
	return Response(json.dumps(msg), status=200,  mimetype="application/json")


@app.route("/login", methods = ['POST'])
def login():
	username = request.form['username']
	password = request.form['password']
	finder = UserFinder.Instance()
	row = finder.findForLogin(username,password)
	if (row):
		mid = row.id
		print 'la id es ', mid
		infoToken = {'token' : generate_auth_token(mid)}
		print 'info token', infoToken
		return Response(json.dumps(infoToken), status=200,  mimetype="application/json")
	return Response(msgNotFound, status=404,  mimetype="application/json")

@app.route("/sponsors", methods = ['GET'])
def getSponsors():
	rows = UserFinder.Instance().findSponsors()
	if (rows): return Response(tuplesToJson(rows), status=200, mimetype="application/json")

@app.route("/sponsorize", methods = ['GET'])
def sponsorize():
	token = request.args.get('token')
	sponsorId, eventId = verify_sponsor_token(token)
	print 'nueva peticion sponsor: ', sponsorId, ' -> evento: ', eventId
	sponsorExists = UserFinder.Instance().findById(sponsorId) != None
	eventExists = EventFinder.Instance().findById(eventId) != None
	if (sponsorExists and eventExists):
		SponsoredGateway(sponsorId, eventId).insert()
		return Response(msgCreatedOK, status=200,  mimetype="application/json")
	else: return Response(msgNoPermission, status=401, mimetype="application/json")

@app.route("/sponsors/<id>/ask", methods = ['POST'])
def askSponsor(id):
	eventId = request.form['eventid']
	token = request.headers['token']
	organizerId = verify_auth_token(token)
	event = EventFinder.Instance().findById(eventId);
	if not organizerId or event.organizerId != organizerId: return Response(msgNoPermission, status=401,  mimetype="application/json")

	#usuario existe y ademas ha organizado el evento
	sponsor = UserFinder.Instance().findById(int(id))
	organizer = UserFinder.Instance().findById(organizerId)

	url = request.url_root + "sponsorize?token=" + generate_sponsor_token(int(id),eventId)
	msg = Message("Eventium", sender="admin@eventium.com", recipients=[sponsor.mail])
	msg.body = "Hola " + sponsor.username + " has recibido una propuesta de " + organizer.username + " con correo " + organizer.mail;
	msg.body += " para patrocinar el evento " + event.title + " ." + "Haz clic en el siguente enlace para confirmar: " + url
	mail.send(msg)
	return Response(msgEmailSent, status = 200,mimetype="application/json")


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

@app.route("/events/recommended", methods = ['GET'])
def getRecommendedEvents():
	token = request.headers['token']
	id = verify_auth_token(token)
	if not id: return Response(msgNoPermission, status=401,  mimetype="application/json")

	categories = CategoriesFinder.Instance().findById(id).categories
	events = EventFinder.Instance().findByCategories(categories)
	return Response(tuplesToJson(events), status=200, mimetype="application/json")


@app.route("/events/<id>", methods = ['DELETE'])
def deleteEvent(id):
	event = EventFinder.Instance().findById(int(id))
	token = request.headers['token']
	organizerId = verify_auth_token(token)
	if not organizerId or event.organizerId != organizerId: return Response(msgNoPermission, status=401,  mimetype="application/json")

	fechaHoy =date.today()
	fechaAux = event.fechai.split('-')
	fechaEvento = date(int(fechaAux[0]), int(fechaAux[1]), int(fechaAux[2]))

	if (fechaEvento > fechaHoy):
		event.delete()
		return Response(msgDeletedOK,status=200, mimetype="application/json")
	else: return Response(msgForbiddenAction, status=403, mimetype="application/json")
	#formato fecha YYYY-MM-DD

#pending 2 campos +
@app.route("/events/<id>", methods = ['PUT'])
def updateEvent(id):
	token = request.headers['token']
	organizerId = verify_auth_token(token)
	if not organizerId: return Response(msgNoPermission, status=401,  mimetype="application/json")

	event = EventFinder.Instance().findById(int(id))
	if(organizerId != event.organizerId) : return Response(msgNoPermission, status=401,  mimetype="application/json")
	print 'oly'
	print event.id
	if request.form.get('title'):
		title = request.form['title']
		event.title = title
		print 'title si'
	if request.form.get('hora_ini'):
		hora_ini = request.form['hora_ini']
		event.horai= hora_ini
		print 'si horai'
	if request.form.get('hora_fin'):
		hora_fin = request.form['hora_fin']
		event.horaf= hora_fin
		print 'si horaf'
	if request.form.get('fecha_ini'):
		fecha_ini = request.form['fecha_ini']
		event.fechai= fecha_ini
		print 'si fechai'
	if request.form.get('fecha_fin'):
		fecha_fin = request.form['fecha_fin']
		event.fechaf= fecha_fin
		print 'si fechaf'
	if request.form.get('precio'):
		precio = request.form['precio']
		event.precio= precio
		print 'si precio'
	if request.form.get('pic'):
		pic = request.form['pic']
		event.pic= pic
		print 'si pic'
	if request.form.get('ciudad'):
		ciudad = request.form['ciudad']
		event.ciudad= ciudad
		print 'si ciudad'
	if request.form.get('categoria'):
		categoria = request.form['categoria']
		event.categoria= categoria
		print 'si categoria'

	if request.form.get('destacado'):
		destacado = request.form['destacado']
		event.destacado= destacado
		print 'si destacado'
	if request.form.get('descripcion'):
		descripcion = request.form['descripcion']
		event.descripcion = descripcion
	if request.form.get('url'):
		url = request.form['url']
		event.url = url
	if request.form.get('nreports'):
		nreports = request.form['nreports']
		event.nreports = nreports
	if request.form.get('direccion'):
		direccion = request.form['direccion']
		event.direccion = direccion
	event.update()
	return Response(msgUpdatedOK, status = 200, mimetype="application/json")

#pending 2 campos +
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

	destacado = False
	descripcion = None
	url = None
	nreports = 0
	direccion = None

	if request.form.get('destacado'):
		destacado = request.form['destacado'] == 'True' 
	if request.form.get('descripcion'):
		descripcion = request.form['descripcion']
	if request.form.get('url'):
		url = request.form['url']
	if request.form.get('nreports'):
		nreports = request.form['nreports']
	if request.form.get('direccion'):
		direccion = request.form['direccion']
	print nreports
	print direccion
	newEvent = EventGateway("", organizerId, title, horaf, horai , fechaf, fechai, precio, pic, ciudad, categoria, destacado, descripcion, url, nreports,direccion)
	error = newEvent.insert()
	if error == None:
		return Response(msgCreatedOK, status = 201, mimetype = "application/json")
	elif error == psycopg2.IntegrityError:
		return Response(msgAlreadyExists, status = 200, mimetype="application/json")
	elif error == psycopg2.DataError:
		return Response(msgTypeError, status = 400, mimetype="application/json")

@app.route("/events/<eventid>/report", methods = ['PUT'])
def reportEvent(eventid):
	finder = EventFinder.Instance()
	event = finder.findById(eventid)
	event.nreports = event.nreports + 1
	event.update()
	if(event.nreports == 5): event.delete()
	return Response(msgUpdatedOK, status = 200, mimetype="application/json")

@app.route("/events/destacados", methods = ['GET'])
def getEventsDestacados():
	rows = EventFinder.Instance().getAllDestacados()
	return Response(tuplesToJson(rows), status = 200, mimetype="application/json")

@app.route("/events/<eventid>/comments", methods = ['GET'])
def getEventsComment(eventid):
	finder = FinderComment.Instance()
	rows = finder.findByEvent(eventid)
	if (rows):
		info = tuplesToJson(rows)
		return Response(info, status=200, mimetype="application/json")
	else:
		return Response(msgNotFound, status=404,  mimetype="application/json")

@app.route("/events/<eventid>/comments", methods = ['POST'])
def postEventComment(eventid):
	token = request.headers['token']
	id = verify_auth_token(token)
	if not id: return Response(msgNoPermission, status=401,  mimetype="application/json")
	
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

#pending to update
@app.route("/events/<eventid>/valoration", methods = ['POST'])
def postEventValoration(eventid):
	token = request.headers['token']
	id = verify_auth_token(token)
	if not id: return Response(msgNoPermission, status=401,  mimetype="application/json")

	points = request.form['points']
	userid = id
	valoration = GatewayValoration(points = points, userid = userid, eventid = eventid)
	error = valoration.insert()
	if error == None:
		return Response(msgCreatedOK, status = 201, mimetype = "application/json")
	elif error == psycopg2.IntegrityError:
		return Response(msgAlreadyExists, status = 200, mimetype="application/json")
	elif error == psycopg2.DataError:
		return Response(msgTypeError, status = 400, mimetype="application/json")

#pending 2 campos mas
@app.route("/events", methods = ['GET'])
def getEvents():

	fecha_ini = request.args.get('fecha_ini')
	fecha_fin = request.args.get('fecha_fin')
	hora_ini = request.args.get('hora_ini')
	hora_fin = request.args.get('hora_fin')
	titulo = request.args.get('titulo')
	precioMin = request.args.get('precioMin')
	precioMax = request.args.get('precioMax')
	ciudad = request.args.get('ciudad')
	categoria = request.args.get('categoria')

	finder = EventFinder.Instance()
	rows = finder.getAll(fecha_ini, fecha_fin, hora_ini, hora_fin, titulo, precioMin, precioMax,ciudad, categoria)
	if (rows): # si no es nulo
		info = tuplesToJson(rows) # rows tiene q ser un conjunto de gateways cualesquiera
		resp = Response(info, status=200, mimetype="application/json")
	else:
		resp = Response(msgNotFound, status=404,  mimetype="application/json")
	return resp

@app.route("/events/<id>", methods = ['GET'])
def getEvent(id):
	finder = EventFinder.Instance()
	row = finder.findById(id)
	if (row):
		info = tupleToJson(row) #row es un gateway cualquiera
		return Response(info, status=200, mimetype="application/json")
	else:
		return Response(msgNotFound, status=404,  mimetype="application/json")	

#queda quitar pssword
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

#Update object user (Add valoration)
@app.route("/users", methods = ['POST'])
def postUser():
	username = request.form['username']
	password = request.form['password']
	mail = request.form['mail']
	pic = request.form['pic']
	ciudad = None
	if (request.form.get('ciudad')):
		ciudad = request.form['ciudad']
	#saldo = request.form['saldo']
	newUser = UserGateway(None, username, password, mail, pic, ciudad=ciudad)
	error = newUser.insert()
	if error == None:
		mid = UserFinder.Instance().findForLogin(username,password).id
		infoToken = {'token' : generate_auth_token(mid)}
		return Response(json.dumps(infoToken), status = 201, mimetype = "application/json")
	elif error == psycopg2.IntegrityError:
		return Response(msgAlreadyExists, status = 200, mimetype="application/json")
	elif error == psycopg2.DataError:
		return Response(msgTypeError, status = 400, mimetype="application/json")

@app.route("/users/<id>", methods = ['PUT'])
def updateUser(id):
	user = UserFinder.Instance().findById(int(id))
	if request.form.get('pic'):
		pic = request.form['pic']
		user.pic = pic
		print 'pic si'
	if request.form.get('password'):
		password = request.form['password']
		user.password = password
		print 'si'
	if request.form.get('verified'):
		verified = request.form['verified']
		user.verified = verified == 'True'
	if request.form.get('banned'):
		banned = request.form['banned']
		user.banned = banned == 'True'
	if (request.form.get('ciudad')):
		user.ciudad = request.form['ciudad']
	user.update()
	return Response(msgUpdatedOK, status = 200, mimetype="application/json")

@app.route("/users/<name>", methods = ['GET'])
def getUser(name):
	finder = UserFinder.Instance()
	row = finder.findByName(name)
	if (row):
		info = tupleToJson(row) #row es un gateway cualquiera
		return Response(info, status=200, mimetype="application/json")
	else:
		return Response(msgNotFound, status=404,  mimetype="application/json")	

#pending to document
@app.route("/users/<id>/events", methods = ['GET'])
def getUserEvents(id):
	finder = EventFinder.Instance()
	row = finder.findByUserId(id)
	if (row):
		info = tuplesToJson(row) #row es un gateway cualquiera
		return Response(info, status=200, mimetype="application/json")
	else:
		return Response(msgNotFound, status=404,  mimetype="application/json")		

@app.route("/users/<id>/follows", methods = ['GET'])
def getUserFollows(id):
	rows = FinderFollowing.Instance().find(id)
	if (rows): # si no es nulo
		info = tuplesToJson(rows) # rows tiene q ser un conjunto de gateways cualesquiera
		resp = Response(info, status=200, mimetype="application/json")
	else:
		resp = Response(msgNotFound, status=404,  mimetype="application/json")
	return resp

@app.route("/users/<id>/follows", methods = ['POST'])
def postUserFollows(id):
	token = request.headers['token']
	id = verify_auth_token(token)
	if not id: return Response(msgNoPermission, status=401,  mimetype="application/json")
	
	followedId = request.form['followed']
	newFollows = GatewayFollowing(id, followedId)
	error = newFollows.insert()
	if error == None:
		return Response(msgCreatedOK, status = 201, mimetype = "application/json")
	elif error == psycopg2.IntegrityError:
		return Response(msgAlreadyExists, status = 200, mimetype="application/json")
	elif error == psycopg2.DataError:
		return Response(msgTypeError, status = 400, mimetype="application/json")

@app.route("/users/<id>/follows/<followed>", methods = ['DELETE'])
def deleteUserFollows(id, followed):
	token = request.headers['token']
	id = verify_auth_token(token)
	if not id: return Response(msgNoPermission, status=401,  mimetype="application/json")

	follows = GatewayFollowing(id, followed)
	error = follows.remove()
	if error == None:
		return Response(msgDeletedOK, status = 201, mimetype = "application/json")
	else:
		return Response(msgNotFound, status=404,  mimetype="application/json")

@app.route("/users/<id>/subscription/<followed>", methods = ['PUT'])
def putUserSubscription(id, followed):
	token = request.headers['token']
	id = verify_auth_token(token)
	if not id: return Response(msgNoPermission, status=401,  mimetype="application/json")

	subscribed = request.form['subscribed']
	finder = FinderFollowing.Instance()
	follows = finder.findSubscription(id,followed)
	follows.subscribed = subscribed == "True"
	error = follows.update()
	if error == None:
		return Response(msgUpdatedOK, status=200, mimetype="application/json")
	else:
		return Response(msgNotFound, status=404,  mimetype="application/json")

@app.route("/users/<id>/wallet", methods = ['PUT'])
def putUserWallet(id):
	token = request.headers['token']
	id = verify_auth_token(token)
	if not id: return Response(msgNoPermission, status=401,  mimetype="application/json")
	
	cardNumber = request.form['card']
	cvc = request.form['cvc']
	money = request.form['money']
	
	user = UserFinder.Instance().findForDeposit(id)

	# esto es provisional
	if user.wallet: user.wallet += int(money)
	else: user.wallet = int(money)
	user.updateWallet()
	return Response(msgUpdatedOK, status=200, mimetype="application/json")
	

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
	
@app.route("/users/<id>/categories", methods = ['GET'])
def getUserCategories(id):
	row = CategoriesFinder.Instance().findById(int(id))
	result = tupleToJson(row)
	return Response(result, status=200, mimetype="application/json")
#pending
@app.route("/users/<id>/calendar", methods = ['POST'])
def addEventToUserCalendar(id):
	token = request.headers['token']
	idCorresponiente = verify_auth_token(token)
	miId = int(id)
	if (miId != idCorresponiente): return Response(msgNoPermission, status=401,  mimetype="application/json")

	row = CalendarGateway(miId,request.form['eventId'])
	error = row.insert()
	if (error == None): return Response(msgCreatedOK,status=200,mimetype="application/json")
	else: return Response(msgIntegrityError,status=400,mimetype="application/json")

#pending
@app.route("/users/<id>/calendar", methods = ['GET'])
def getEventsFromUserCalendar(id):
	token = request.headers['token']
	idCorresponiente = verify_auth_token(token)
	miId = int(id)
	if (miId != idCorresponiente): return Response(msgNoPermission, status=401,  mimetype="application/json")
	rows = CalendarFinder.Instance().getByUserId(miId)
	info = tuplesToJson(rows)
	return Response(info,status=200,mimetype="application/json")

#pending
@app.route("/users/<id>/calendar/<eventid>", methods = ['DELETE'])
def deleteEventsFromUserCalendar(id, eventid):
	token = request.headers['token']
	idCorresponiente = verify_auth_token(token)
	miId = int(id)
	if (miId != idCorresponiente): return Response(msgNoPermission, status=401,  mimetype="application/json")
	entry = CalendarFinder.Instance().getEntry(int(id),int(eventid))
	entry.delete()
	return Response(msgDeletedOK,status=200,mimetype="application/json")
if __name__ == "__main__":
	while True:
		try:
			app.run(use_reloader = False, debug = True)
		except:
			pass
