import sqlite3
import random

DB_FILE = "data.db"

#check for user_id in data
def user_exists(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM user WHERE user_id = ?", (username,))
    result = c.fetchone() != None
    db.close()
    return result

#check for right password in data
def login(username, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT password FROM user where user_id = ?", (username,))
    pw = c.fetchone()[0]
    db.close()
    return pw == password

#checks if username already in data
def user_exists(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM user WHERE user_id = ?", (username,))
    result = c.fetchone() != None
    db.close()
    return result

#registers (fails if user already exists, is empty)
def register(username, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if (username.strip() == "" or password.strip() == ""):
        db.close()
        return "Username or password cannot be empty."
    if user_exists(username):
        db.close()
        return "Username is already taken."
    c.execute("INSERT INTO user (user_id, password) VALUES (?, ?)", (username, password))
    db.commit()
    db.close()
    return "Registered"
