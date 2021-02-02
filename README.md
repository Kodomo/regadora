# Regadora 1.0

Control de bomba de regad√o usando Raspberry Pi. La insterfaz web es gestionada usando Flask

## Install

`sudo apt install python3-pip git`

`pip3 install -r web/requirements.txt`

## DB init

`python3 createdb.py`

Dependiendo de cuales sean las salidas, es necesario ajustar el numero del pin GPIO en el archivo `createdb.py`

## Debug Run

`python3 app.py`

Puedes acceder via web y accionar el motor de la bomba. Se deben ajustar los diferentes valores de encendido y apagado dependiendo de los requerimientos. La implementaci√n permite configurar ciclos autom√ticos de prendido y apagarlo, pero a√n carece de la GUI para ello. Tambi√n genera un registro de cada vez que cambia un est√do en los pines del GPIO.
