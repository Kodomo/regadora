# -*- coding: utf-8 -*-
import os
from flask import Flask, Blueprint, request, render_template, send_from_directory, redirect, url_for
from user_agents import parse
from .modelo import Estado, Timers, Historial
from . import db

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    return redirect(url_for('main.dashboard'))

@main.route('/about')
def about():
    return render_template('license.html')

@main.route('/prender/<int:gpio>/')
def prender(gpio):
    new = Timers(pin=gpio, timeon=10, timeoff=10, repeat=0)
    db.session.add(new)
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard')
def dashboard():
    
    return render_template('dashboard.html', title='Datos del Navegador')

@main.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

