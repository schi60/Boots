# Sophia Chi, Emaan Asif, Junjie Li
# SoftDev
# P01

from flask import Flask, render_template, request, flash, redirect, session, url_for
from db import select_query, insert_query, general_query

app = Flask(__name__)

import auth
app.register_blueprint(auth.bp)

@app.before_request
def check_authentification():
    if 'username' not in session.keys() and request.blueprint != 'auth' and request.endpoint != 'static':
        flash("Please log in to view our website", "error")
        return redirect(url_for("auth.login_get"))

# displays all blogs
@app.get('/home')
def home_get():
    return render_template('frontlawn.html')

@app.get('/bedroom')
def bedroom_get():
    return render_template('bedroom.html')

@app.get('/kitchen')
def kitchen_get():
    return render_template('kitchen.html')

@app.get('/livingRoom')
def livingRoom_get():
    return render_template('livingRoom.html')

@app.get('/settings')
def settings_get():
    return render_template('settings.html')