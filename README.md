# PES-Eventium-Backend
IP server 10.4.41.168
sudo service postgresql restart - reinicia la BD en el server

### COMO FUNCIONA EL LOGIN ###

- Hacer una peticion POST a /login con campos en form username y password.
- La peticion anterior (si es correcta) devuelve un token, si no un error 404.
- El token se pasa en el header (nombre token) a las peticiones q requieran autentificacón.

### OTRAS COSAS ###
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
