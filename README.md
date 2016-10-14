# PES-Eventium-Backend
La versión de python que usamos es la 2.7.X

- Tutorial para postgres con python 
 - https://www.tutorialspoint.com/postgresql/postgresql_python.htm
 - http://initd.org/psycopg/docs/usage.html#passing-parameters-to-sql-queries

- Para iniciar el server en modo local simplemente hacer: 
"python eventium.py" (por defecto la conexión se establece en localhost:5000 === 127.0.0.1:5000)

- Para iniciar el server en el servidor de la fib hacer
"
 - "export FLASK_APP=eventium.py"
 - "python -m flask run --host=0.0.0.0"
poner host 0.0.0.0 implica que el server ahora es accesible a través de la ip del ordenador.
"

- Librerías que usamos:
 - flask (librería que proporciona el server)
 - psycopg2 (librería de postresql para python)
