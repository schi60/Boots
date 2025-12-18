# Sophia Chi, Emaan Asif, Junjie Li
# SoftDev
# P01

from flask import Flask, render_template, request, flash, redirect, session, url_for
from db import select_query, insert_query, general_query
import urllib.request, json, random

app = Flask(__name__)
app.secret_key = "edkasifjdsufh"

import auth
app.register_blueprint(auth.bp)

@app.before_request
def check_authentification():
    if 'username' not in session and request.blueprint != 'auth' and request.endpoint != 'static':
        flash("Please sign up to view our website", 'info')
        return render_template('auth/register.html')

#home
@app.get('/')
def startPage_get():
    return render_template('startPage.html')

#map
@app.get('/map')
def map_get():
    return render_template('map.html')

#frontLawn
@app.get('/lawn')
def frontLawn_get():
    return render_template('frontlawn.html')

#bedroom
@app.get('/bedroom')
def bedroom_get():
    #jokeAPI
    with urllib.request.urlopen("https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit ") as response:
        jokeData = json.loads(response.read())

    if jokeData.get("type") == "single":
        jokeText = jokeData.get("joke")
    else:
        jokeText = f"{jokeData.get('setup')} - {jokeData.get('delivery')}"

    #metAPI
    with urllib.request.urlopen(
        "https://collectionapi.metmuseum.org/public/collection/v1/search?q=dog&hasImages=true"
    ) as response:
        metData = json.loads(response.read())

    metObject = {}
    if metData.get("objectIDs"):
        objectId = random.choice(metData["objectIDs"])
        objectUrl = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{objectId}"
        with urllib.request.urlopen(objectUrl) as response:
            metObject = json.loads(response.read())

    return render_template('bedroom.html', joke=jokeText, metItem=metObject)

#kitchen
with open('keys/key_HolidaysAPI.txt') as file:
    holidaysKey = file.read().strip()

@app.get('/kitchen')
def kitchen_get():
    #recipeAPI
    with urllib.request.urlopen("https://www.themealdb.com/api/json/v1/1/random.php") as response:
        recipesData = json.loads(response.read())

    #holidaysAPI
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    holidaysUrl = (
        f"https://holidays.abstractapi.com/v1/"
        f"?api_key={holidaysKey}&country=US&year=2025"
        f"&month={month}&day={day}")
    with urllib.request.urlopen(holidaysUrl) as response:
        holidaysData = json.loads(response.read())
    holidaysText = None
    if isinstance(holidaysData, list) and len(holidaysData) > 0:
        holidaysText = holidaysData[0].get("name")

    return render_template('kitchen.html', recipes=recipesData, holidays=holidaysText)

#livingRoom
with open('keys/key_MoviesAPI.txt') as file:
    movieKey = file.read().strip()

with open('keys/key_TheCatAPI.txt') as file:
    catKey = file.read().strip()

@app.get('/livingRoom')
def livingRoom_get():
    #moviesAPI
    with urllib.request.urlopen(f"https://www.omdbapi.com/?apikey={movieKey}&s=mystery") as response:
        movies = json.loads(response.read())

    #catAPI
    catRequest = urllib.request.Request(
        "https://api.thecatapi.com/v1/images/search?has_breeds=1",
        headers={"x-api-key": catKey})
    with urllib.request.urlopen(catRequest) as response:
        catData = json.loads(response.read())
    catImage = None
    if isinstance(catData, list) and len(catData) > 0:
        catImage = catData[0].get("url")

    return render_template('livingRoom.html', movies=movies, catImage=catImage)

#settings
@app.get('/settings')
def settings_get():
    return render_template('settings.html', username=session.get('username'))

#register
@app.get('/register')
def sign_up():
    return render_template('/auth/register.html')

if __name__ == '__main__':
    app.run(debug=True)
