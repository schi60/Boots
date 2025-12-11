# Sophia Chi, Emaan Asif, Junjie Li
# SoftDev
# P01

from flask import Flask, render_template, request, flash, redirect, session, url_for
from db import select_query, insert_query, general_query
import urllib.request, json

app = Flask(__name__)
app.secret_key = "edkasifjdsufh"

import auth
app.register_blueprint(auth.bp)

@app.get('/login')
def check_authentification():
    if 'username' not in session.keys() and request.blueprint != 'auth' and request.endpoint != 'static':
        flash("Please log in to view our website", "error")
        return redirect(url_for("auth.login_get"))

#frontlawn
@app.get('/')
def home_get():
    return render_template('frontlawn.html')

#bedroom
@app.get('/bedroom')
def bedroom_get():
    #jokeAPI
    with urllib.request.urlopen("https://v2.jokeapi.dev/joke/Any") as response:
        jokeData = json.loads(response.read())
    if jokeData.get("type") == "single":
        jokeText = jokeData.get("joke")
    else:
        jokeText = f"{jokeData.get('setup')} - {jokeData.get('delivery')}"

    #metAPI
    with urllib.request.urlopen("https://collectionapi.metmuseum.org/public/collection/v1/search?q=cat") as response:
        metData = json.loads(response.read())
    metObject = {}
    if metData.get("objectIDs"):
        objectId = metData["objectIDs"][0]
        objectUrl = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{objectId}"
        with urllib.request.urlopen(objectUrl) as response:
            metObject = json.loads(response.read())

    return render_template('bedroom.html', joke=jokeText, met_item=metObject)

#kitchen
#with open('keys/key_HolidaysAPI.txt') as file:
    holidaysKey = file.read().strip()

@app.get('/kitchen')
def kitchen_get():
    #freeRecipeAPI
    recipeUrl = "https://www.themealdb.com/api/json/v1/1/random.php"
    with urllib.request.urlopen(recipeUrl) as response:
        recipesData = json.loads(response.read())
    return render_template('kitchen.html', recipes=recipesData)

    #holidaysAPI
    holidaysUrl =  f'https://holidays.abstractapi.com/v1/?api_key={holidaysKey}&country=US&year=2025&month=12&day=25'
    with urllib.request.urlopen(holidaysUrl) as response:
        holidaysData = json.loads(response.read())

    return render_template('kitchen.html', recipes=recipesData, holidays=holidaysData)

#livingRoom
with open('keys/key_MoviesAPI.txt') as file:
    movieKey = file.read().strip()

with open('keys/key_TheCatAPI.txt') as file:
    catKey = file.read().strip()

@app.get('/livingRoom')
def livingRoom_get():
    #movieAPI
    movieUrl = f"https://www.omdbapi.com/?apikey={movieKey}&s=mystery"
    with urllib.request.urlopen(movieUrl) as response:
        movies = json.loads(response.read())
    catUrl = "https://api.thecatapi.com/v1/images/search?has_breeds=1"
    catRequest = urllib.request.Request(cat_url, headers={"x-api-key": catKey})

    #catAPI
    with urllib.request.urlopen(catRequest) as response:
        catData = json.loads(response.read())
    catImage = None
    if isinstance(catData, list) and len(catData) > 0:
        catImage = catData[0].get("url")

    return render_template('livingRoom.html', movies=movies, catImage=catImage)

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
