# PES-Eventium-Backend
IP server 10.4.41.168


### COMO FUNCIONA EL LOGIN ###

hacer una peticion POST a /login. campos del form username y password.
esto devuelve un token
este token se pasa en el header poniendo el nombre token
si no es válido devuelve un error http 401

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
 - itsdangerous (para la gestion de token)

- Forzar cierre del proceso python flask en windows desde cmd:
 - "Taskkill /IM python.exe /F"

- Provar recurso Test de la API del server:
 - Tener la VPN activada
 - tener el proceso de flask corriendo (ver paso de iniciar el server en el servidor de la fib)
 - de momento se puede:
 
  - 10.4.41.168:5000/tests <- GET
  - 10.4.41.168:5000/test/id <- aqui poner el id del test
  - 10.4.41.168/test <- POST (poner en el body los campos id, num, data son respectivamente int, int, y string
