# Boots
# Softdev 2025
# p01

from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
DB_FILE = "user.db"

def setup_database():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            session_key TEXT,
            login_token TEXT
        );
    """)
    db.commit()
    db.close()
setup_database()

@app.route("/login", methods=["GET", "POST"])
def disp_login():
    if request.method == 'POST':
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        username = request.form["username"]
        password_form = request.form["password"]
        c.execute("SELECT password FROM users WHERE username = ?", (username,))
        user_data = c.fetchone()
        db.close()
        if user_data:
            passworddb = user_data[0]
            if password_form == passworddb:
                session["username"] = username
                return redirect(url_for('disp_homepage'))
            else:
                flash("Incorrect password. Try again.")
        else:
            flash("Username incorrect or not found. Try again.")
        return redirect(url_for('disp_login'))
    return render_template('login.html')


@app.route("/logout")
def disp_logout():
    session.pop('username', None)
    return render_template('logout.html')
	
@app.route("/createaccount", methods = ['GET', "POST"])
def set_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_exists = c.fetchone()
        if user_exists:
            db.close()
            flash("Username already taken!")
            return redirect(url_for('set_user'))
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password))
        db.commit()
        db.close()
        session['username'] = username
        return redirect(url_for('disp_homepage'))
    return render_template('createaccount.html')

@app.route("/")
def disp_homepage():
    return render_template('homepage.html')

if __name__ == "__main__":
    app.debug = True
    app.run()