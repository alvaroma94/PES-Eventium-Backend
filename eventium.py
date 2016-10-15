from flask import Flask
import sys
sys.path.append('./pruebasBD')
from connection import Connection
import psycopg2


app = Flask(__name__)

connection = Connection.Instance()
connection.connect()

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/tests", methods = ['GET'])
def getTests():
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM test")
	ret = cursor.fetchall()
	cursor.close()
	print ret
	return 'ok'

@app.route("/test", methods = ['POST'])
def postTest():
	#intento crear la tabla
	try:
		cursor = connection.cursor()
		cursor.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
	except psycopg2.ProgrammingError as err:
		print err
		cursor.close()
		connection.rollback()

	print 'a'
	cursor = connection.cursor()
	cursor.execute("INSERT INTO test (num, data) VALUES (%s, %s)",(100, "abc'def"))
	connection.commit()
	cursor.close()
	return "OK"

if __name__ == "__main__":
	while True:
		try:
			app.run(use_reloader = False)
		except:
			pass
