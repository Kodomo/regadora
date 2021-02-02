from sqlalchemy.sql import func
from sqlalchemy.dialects import sqlite
from web import db


class Historial(db.Model):
    __tablename__ = 'historial'

    id          = db.Column(db.BigInteger().with_variant(sqlite.INTEGER(), 'sqlite'), primary_key=True, autoincrement=True)
    ts          = db.Column(db.DateTime(timezone=True), server_default=func.now())
    trigger     = db.Column(db.String(50))
    mensaje     = db.Column(db.String(50))


class Estado(db.Model):
    __tablename__ = 'pines'

    id          = db.Column(db.BigInteger().with_variant(sqlite.INTEGER(), 'sqlite'), primary_key=True, autoincrement=True)
    pin        = db.Column(db.Integer, nullable=False, unique=True)

    laston      = db.Column(db.DateTime(timezone=True), server_default=func.now())
    lastoff     = db.Column(db.DateTime(timezone=True), server_default=func.now())

    curval      = db.Column(db.Integer, nullable=False, default=0)


class Timers(db.Model):
    __tablename__ = 'timers'

    id          = db.Column(db.BigInteger().with_variant(sqlite.INTEGER(), 'sqlite'), primary_key=True, autoincrement=True)

    pin        = db.Column(db.Integer, nullable=False)

    timeon      = db.Column(db.Integer, nullable=False, default=60)
    timeoff     = db.Column(db.Integer, nullable=False, default=0)

    repeat      = db.Column(db.Integer, nullable=False, default=0)

