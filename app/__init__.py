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

#allowed endpoints
@app.before_request
def check_authentification():
    allowedEndpoints = ['static', 'startPage_get', 'auth.login_get', 'auth.login_post', 'auth.signup_get', 'auth.signup_post']
    if 'username' not in session and request.endpoint not in allowedEndpoints:
        flash("Please log in to view our website", 'info')
        return redirect(url_for('auth.login_get'))

#home
@app.get('/')
def startPage_get():
    win = session.get('correct', False)
    success= None
    if win and 'success' in session:
        success = session.pop('success')
    return render_template('startPage.html', win=win, success=success)

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

#collecting clues 
def collectClue(username, clueID):
    if 'collectedClues' not in session:
        session['collectedClues'] = []
    existing = select_query("SELECT * FROM clues WHERE username=? AND clueID=?", [username, clueID])  
    if not existing:
        insert_query("clues", {"username": username, "clueID": clueID})
        session['collectedClues'].append(clueID)
        session.modified = True
        return True
    return False

@app.post('/clue/<clueID>')
def clue(clueID):
    if 'username' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('auth.login_get'))
    collectClue(session['username'], clueID)
    return redirect(request.referrer or url_for('map_get'))

#all clues have been collected
def allClues():
    return len(session.get('collectedClues', [])) >= 6

#game reset
def reset():
    session.pop('collectedClues', None)
    session.pop('accusationMade', None)
    session.pop('correct', None)
    session.pop('success', None)  
    session.modified = True

@app.get('/reset')
def reset_get():
    if 'username' not in session:
        return redirect(url_for('auth.login_get'))
    reset()
    flash('Game reset! Start collecting clues again.', 'info')
    return redirect(url_for('startPage_get'))

#game end
@app.get('/accusation')
def accusation():
    if 'username' not in session:
        return redirect(url_for('auth.login_get'))
    if not allClues():
        flash('You need all 6 clues to make an accusation!', 'error')
        return redirect(url_for('frontLawn_get'))
    return render_template('finalAccusation.html')

@app.post('/submit')
def submit():
    if 'username' not in session:
        return redirect(url_for('auth.login_get')) 
    if not allClues():
        flash('You need all 6 clues first!', 'error')
        return redirect(url_for('frontLawn_get')) 
    murderer = request.form.get('murderer') 
    if murderer == 'butler':
        session['accusation_made'] = True
        session['correct'] = True
        session['success'] = (
            "CORRECT! The Butler killed Reginald. He was stealing art and got caught. "
            "Click the button below to return to the start page."
        )
        session.modified = True
        return render_template('finalAccusation.html', correct=True, clues=session.get('collectedClues', [])) 
    else:
        reset()
        wrong_messages = {
            'dealer': "Wrong! Vivian had motive but not opportunity. She left before the murder.",
            'nephew': "Wrong! Miles wanted the inheritance but was at the casino during the murder.",
            'cook': "Wrong! Mrs. Henderson was angry, but her son's issues weren't worth murder.",
            'rival': "Wrong! Dr. Finch wanted the dagger, but museum cameras confirm his alibi."
        }
        flash(f"{wrong_messages.get(murderer, 'Wrong answer')} All clues have been cleared. Start over.", 'error')
        return render_template('startPage.html', correct=False, clues=[])

if __name__ == '__main__':
    app.run(debug=True)