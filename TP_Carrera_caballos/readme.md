EJECUCION DEL PROGRAMA
DESDE EL DIRECORIO RAIZ (/TP_CARRERA_CABALLOS)
$python -m app.main


EJECUCION DE LOS TESTS
DESDE EL DIRECORIO RAIZ (/TP_CARRERA_CABALLOS)
$pytest tests/


RUTAS DE POSTMAN:
EN LA CARPETA "POSTMAN" DEJE 4 COLECCIONES QUE SON LAS UTILIZADAS EN LA PRUEBA EN VIVO


---------------------------------------------------------

IMPORTANTE PARA ENTENDER EL MODELO DE CASINO

- El usuario administrador se crea al crear un usuario de dni "admin", es un unico usuario administrador que va a tener un token que lo habilite a crear y modificar entidades

---------------------------------------------------------


- Mi modelo de casino basa cuanto paga cada caballo en base a su "frecuencia de victoria", esta frecuencia es un numero entre 1 y 10 que estima cada cuantas carreras realiza una victoria. Se define al momento de crear el caballo.
es decir:
El caballo "A" con una frecuencia de "2" sinificaria que gana 1 de cada 2 carreras aproximadamente
el caballo "B" con una frecuencia de "7" significaria que gana 1 de cada 7 carreras aproximadamente

este numero afecta en dos momentos. 

1)- Al definir un ganador: En el momento que se define un ganador, un caballo con una frecuencia de 2 tiene ventaja sobre uno que tiene frecuencia de 7 (Este algoritmo esta definido en el modelo de "Caballo", alli se explica un poco mejor). SIN EMBARGO, eso no significa que el de menor frecuencia siempre vaya a ganar, sino que unicamente tiene mas chances.

2)- Al otorgar un multiplicador de dinero: A mayor numero de frecuencia significa una menor posibilidad de ganar, por ende el multiplicador de dinero sube

---------------------------------------------------------