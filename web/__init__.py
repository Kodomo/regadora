import threading
import atexit
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config


POOL_TIME = 5 #Seconds

# variables that are accessible from anywhere
commonDataStruct = {}
# lock to control access to variable
dataLock = threading.Lock()
# thread handler
yourThread = threading.Thread()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    import RPi.GPIO as gpio

    def interrupt():
        global yourThread
        import datetime
        from .modelo import Estado, Timers, Historial
        yourThread.cancel()

        with app.app_context():
            for gpioPin in Estado.query.filter(Estado.curval==1).all():
                gpio.output(gpioPin.pin, gpio.LOW)
                gpioPin.curval = 0
                gpioPin.laston = datetime.datetime.now()
                db.session.flush()
            for timer in Timers.query.all():
                db.session.delete(timer)
                db.session.flush()
            gpio.cleanup()
            msg = Historial(trigger='shutdown', mensaje='Apagado')
            db.session.add(msg)
            db.session.commit()
        
#        yourThread.cancel()

    def doStuff():
        global commonDataStruct
        global yourThread
        import datetime
        from .modelo import Estado, Timers, Historial
        with dataLock:
        # Do your stuff with commonDataStruct Here
            with app.app_context():
                ts = datetime.datetime.now()
                for timer in Timers.query.all():
                    tn = datetime.timedelta(seconds=timer.timeon)
                    tf = datetime.timedelta(seconds=timer.timeoff)
                    
                    nextoff = ts - tn
                    nexton  = ts - tf

                    turnon = Estado.query.filter(Estado.curval==0, Estado.laston<nexton).one_or_none()
                    if turnon is not None:
                        turnon.curval = 1
                        turnon.lastoff = ts
                        gpio.output(turnon.pin, gpio.HIGH)
                        msg = Historial(trigger='timer', mensaje='{} encendido'.format(Estado.pin))
                        db.session.add(msg)
                        db.session.flush()
                    else:
                        turnoff = Estado.query.filter(Estado.curval==1, Estado.lastoff<nextoff).one_or_none()
                        if turnoff is not None:
                            gpio.output(turnoff.pin, gpio.LOW)
                            turnoff.curval = 0
                            turnoff.laston = ts
                            msg = Historial(trigger='timer', mensaje='{} apagado'.format(Estado.pin))
                            db.session.add(msg)
                            if timer.repeat > 0:
                                timer.repeat = timer.repeat - 1
                            if timer.repeat <= 0:
                                db.session.delete(timer)
                                msg = Historial(trigger='timer', mensaje='repeticiones alcanzadas')
                                db.session.add(msg)
                            
                            db.session.flush()
                    
                    db.session.commit()


        # Set the next thread to happen
        yourThread = threading.Timer(POOL_TIME, doStuff, ())
        yourThread.start()   

    def doStuffStart():
        # Do initialisation stuff here
        global yourThread
        # Create your thread
        yourThread = threading.Timer(POOL_TIME, doStuff, ())
        yourThread.start()
        gpio.setmode(gpio.BCM)
        with app.app_context():
            from .modelo import Estado
            for puerta in Estado.query.all():
                gpio.setup(puerta.pin, gpio.OUT)

    # Initiate
    doStuffStart()
    # When you kill Flask (SIGTERM), clear the trigger for the next thread
    atexit.register(interrupt)
    
    
    from .regadoraweb import main
    app.register_blueprint(main)

    return app

app = create_app()
