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

# collecting clues
def collect_clue(clue_id):
    """Add a clue to the user's collected clues in session"""
    if 'collected_clues' not in session:
        session['collected_clues'] = []
    
    if clue_id not in session['collected_clues']:
        session['collected_clues'].append(clue_id)
        session.modified = True
        return True
    return False

def has_all_clues():
    """Check if user has collected all 6 clues"""
    return len(session.get('collected_clues', [])) >= 6

def reset_game():
    # Lose all progress
    session.pop('collected_clues', None)
    session.pop('accusation_made', None)
    session.pop('accusation_correct', None)
    session.pop('success_message', None)  # Clear any stored success message
    session.modified = True

@app.before_request
def check_authentification():
    # Skip auth check for these endpoints
    allowed_endpoints = ['static', 'startPage_get', 'auth.login_get', 
                         'auth.login_post', 'auth.signup_get', 'auth.signup_post',
                         'collect_clue_route', 'reset_game_route', 'submit_final_answer',
                         'final_accusation']
    
    if 'username' not in session and request.endpoint not in allowed_endpoints:
        flash("Please log in to view our website", 'info')
        return redirect(url_for('auth.login_get'))

#home
@app.get('/')
def startPage_get():
    # Check if user just won the game
    won_game = session.get('accusation_correct', False)
    
    # Get the success message from session if it exists
    success_message = None
    if won_game and 'success_message' in session:
        success_message = session.pop('success_message')
    
    return render_template('startPage.html', won_game=won_game, success_message=success_message)

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
        #    insert_query("artwork", {'art': metObject})

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

@app.post('/collect-clue/<clue_id>')
def collect_clue_route(clue_id):
    if 'username' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('auth.login_get'))
    
    # Just collect the clue without flashing a message
    collect_clue(clue_id)
    
    # Return to the previous page (the room where the clue was collected)
    return redirect(request.referrer or url_for('map_get'))

@app.get('/reset-game')
def reset_game_route():
    if 'username' not in session:
        return redirect(url_for('auth.login_get'))
    
    reset_game()
    flash('Game reset! Start collecting clues again.', 'info')
    return redirect(url_for('startPage_get'))

@app.get('/final-accusation')
def final_accusation():
    if 'username' not in session:
        return redirect(url_for('auth.login_get'))
    
    # Check if they have all clues
    if not has_all_clues():
        flash('You need all 6 clues to make an accusation!', 'error')
        return redirect(url_for('frontLawn_get'))
    
    return render_template('final_accusation.html')

@app.post('/submit-final-answer')
def submit_final_answer():
    if 'username' not in session:
        return redirect(url_for('auth.login_get'))
    
    # Check if they have all clues (prevent direct URL access)
    if not has_all_clues():
        flash('You need all 6 clues first!', 'error')
        return redirect(url_for('frontLawn_get'))
    
    murderer = request.form.get('murderer')
    
    # CORRECT ANSWER: The butler did it!
    if murderer == 'butler':
        # Mark accusation as made and correct (but DON'T reset game)
        session['accusation_made'] = True
        session['accusation_correct'] = True
        
        # Store success message in session to display on start page
        session['success_message'] = '🎉 CORRECT! James Worthington (the butler) killed Reginald. He was stealing art and got caught. Case solved!'
        session.modified = True
        
        # REMOVED THE FLASH() CALL HERE - we're using session message instead
        # flash(session['success_message'], 'success')  # DELETE THIS LINE
        
        return redirect(url_for('startPage_get'))
    else:
        # WRONG ANSWER - Reset game immediately for losers
        reset_game()
        
        # Different messages for different wrong answers
        wrong_messages = {
            'dealer': "❌ Wrong! Vivian had motive but not opportunity. She left before the murder.",
            'nephew': "❌ Wrong! Miles wanted the inheritance but was at the casino during the murder.",
            'cook': "❌ Wrong! Mrs. Henderson was angry, but her son's issues weren't worth murder.",
            'rival': "❌ Wrong! Dr. Finch wanted the dagger, but museum cameras confirm his alibi."
        }
        
        flash(f"{wrong_messages.get(murderer, '❌ Wrong answer!')} The case has been reset. Start over!", 'error')
        return redirect(url_for('startPage_get'))
		 
if __name__ == '__main__':
    app.run(debug=True)