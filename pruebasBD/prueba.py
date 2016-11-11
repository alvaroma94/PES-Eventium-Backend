from utilsBD import UtilsBD
from connection import Connection
from gatewayTest import GatewayTest


#en el server se haria
c = Connection.Instance().connect()

query = "SELECT * FROM test WHERE id = %s"
values = (1,)
u = UtilsBD.Instance()
t = u.executeSelect(query,values, True)
print t

query = "INSERT INTO test (id, num, data) VALUES (%s ,%s, %s)"
values = (1, 6, 'hola')
print UtilsBD.Instance().executeInsert(query,values)

newTest = GatewayTest(2,6,'k')
print newTest.insert()