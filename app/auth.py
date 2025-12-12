# Sophia Chi, Emaan Asif, Jun Jie Li
# SoftDev
# P01
# Dec 2025

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import select_query, insert_query
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.get('/signup')
def signup_get():
    return render_template('auth/register.html')

@bp.post('/signup')
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    if len(select_query("SELECT * FROM profiles WHERE username=?", [username])) != 0:
        flash('Username already exists.', 'error')
        return redirect(url_for('auth.signup_get'))
    hashed_password = generate_password_hash(password)
    insert_query("profiles", {"username": username, "password": hashed_password})
    flash('Sign up successful! Please log in.', 'success')
    return redirect(url_for('auth.login_get'))

@bp.get('/login')
def login_get():
    return render_template('auth/login.html')

@bp.post('/login')
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    rows = select_query("SELECT * FROM profiles WHERE username=?", [username])
    if len(rows) != 0 and check_password_hash(rows[0]['password'], password):
        session['username'] = username
        flash(f'Welcome back, {username}!', 'success')
        return redirect(url_for('map_get'))
    else:
        flash('Invalid username or password.', 'error')
        return redirect(url_for('auth.login_get'))

@bp.get('/logout')
def logout_get():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('startPage_get'))
