import psycopg2
import json
import SingletonPattern



@SingletonPattern.Singleton
class Connection: 
	#esta clase representa una instancia de conexion a la BD
	#los metodos de esta clase se llaman igual q la clase connection de la libreria
	#para simplificar su uso
	
	def __init__(self):
		self.connected = False
		pass #este metodo se llama automaticamente, es la constructora, no hace nada
	
	def disconnect(self):
		#la variable conn es implicita
		self.conn.close()
		print "connection ended"

	def connect(self):
		'''
 		el fichero de configuracion tiene q estar en la misma carpeta q este script
 		el server tendra el suyo propio
 		cada uno q se lo configure a su gusto
 		'''
 		if (not self.connected):
	 		print "attempting connection ..."
			configFile = open("dbConfig.json")
			if (not configFile): #si no existe el fichero
				raise ValueError("dbCOnfig.json not found")
			config = json.loads(configFile.read())
			configFile.close()
			# la variable conn es implicita
			self.conn = psycopg2.connect(database=config['database'], user=config['user'], 
							password=config['password'], host=config['host'],
						    port=config['port'])
			print 'connection started'
			self.connected = True

	def commit(self): #se aplican realizados hasta ahora en la BD
		self.conn.commit()

	def cursor(self):
		#no se olviden de cerrarlo cuando hayan acabado de usarlo
		return self.conn.cursor()

	def rollback(self):
		self.conn.rollback()


'''
c = Connection.Instance()
c.connect()

try:
	cursor = c.cursor()
	cursor.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
except psycopg2.ProgrammingError as err:
	print err
	c.rollback()


cursor.execute("INSERT INTO test (num, data) VALUES (%s, %s)",(100, "abc'def"))
c.commit() #im


cursor.execute("SELECT * FROM test")
print cursor.fetchall() #devuelve todas las tuplas

cursor.close()
c.disconnect()
'''



