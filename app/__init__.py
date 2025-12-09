# Sophia Chi, Emaan Asif, Junjie Li
# SoftDev
# P01

from flask import Flask, render_template, request, flash, redirect, session, url_for
from db import select_query, insert_query, general_query
import sqlite3, urllib, json

app = Flask(__name__)
app.secret_key = "edkasifjdsufh"

import auth
app.register_blueprint(auth.bp)

@app.get('/login')
def check_authentification():
    if 'username' not in session.keys() and request.blueprint != 'auth' and request.endpoint != 'static':
        flash("Please log in to view our website", "error")
        return redirect(url_for("auth.login_get"))

#home
@app.get('/')
def home_get():
    return render_template('frontlawn.html')

#bedroom
@app.get('/bedroom')
def bedroom_get():
    return render_template('bedroom.html')

#kitchen
with open('keys/key_HolidaysAPI.txt') as file:
    api_key = file.read()

@app.get('/kitchen')
def kitchen_get():
    with urllib.request.urlopen(f'{api_key}') as response:
        data = response.read()
    data = json.loads(data)
    return render_template('kitchen.html',image_link=data["hdurl"], explanation=data["explanation"])

#livingRoom
with open('keys/key_MoviesAPI.txt') as file:
    api_key0 = file.read()

with open('keys/key_TheCatAPI.txt') as file:
    api_key1 = file.read()

@app.get('/livingRoom')
def livingRoom_get():
    with urllib.request.urlopen(f'https://www.omdbapi.com/?s={api_key}') as response:
       data = response.read()
    data = json.loads(data)

    with urllib.request.urlopen(f'{api_key}') as response:
       data = response.read()
    data = json.loads(data)
    return render_template('livingRoom.html',image_link=data["hdurl"], explanation=data["explanation"])

#settings
@app.get('/settings')
def settings_get():
    return render_template('settings.html')

#register
@app.get('/register')
def sign_up():
    return render_template('/auth/register.html')

if __name__ == '__main__':
    app.run(debug=True)
