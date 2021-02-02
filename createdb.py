from web import create_app, db
from web.modelo import Estado

iapp = create_app()


with iapp.app_context():
    db.create_all()
    motor = Estado(pin=18)
    db.session.add(motor)
    db.session.commit()
