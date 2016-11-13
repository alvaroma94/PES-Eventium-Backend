from flask import Flask, Response, request
import sys
import psycopg2
sys.path.append('./pruebasBD')
from utilsBD import UtilsBD
from connection import Connection


#en el server se haria
c = Connection.Instance().connect()

# Open a file
fo = open("./Schema/test.txt", "r")
str = fo.read();
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
sqlCommands = str.split(';')
print sqlCommands
for command in sqlCommands[1:-1]:
	print command
	try:
		cursor = c.cursor()
		cursor.execute(command)
		c.commit()
		cursor.close()
	except Exception, e:
		print e
		Connection.Instance().rollback()



cursor.close()
'''
	cursor.execute("CREATE SCHEMA public;")
cursor.close()
'''
'''
query = "DROP SCHEMA public CASCADE;"
u = UtilsBD.Instance()
t = u.executeRemove(query,None, True)
print t
'''
'''query = "INSERT INTO test (id, num, data) VALUES (%s ,%s, %s)"
values = (1, 6, 'hola')
print UtilsBD.Instance().executeInsert(query,values)

newTest = GatewayTest(2,6,'k')
print newTest.insert()'''