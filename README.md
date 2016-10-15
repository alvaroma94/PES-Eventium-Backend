# PES-Eventium-Backend
IP server 10.4.41.147

La versión de python que usamos es la 2.7.X

- Tutorial para postgres con python 
 - http://initd.org/psycopg/docs/usage.html
 - https://www.tutorialspoint.com/postgresql/postgresql_python.htm

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

- Forzar cierre del proceso python flask en windows desde cmd:
 - "Taskkill /IM python.exe /F"
