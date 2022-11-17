from flask_app.models import user_model
from flask_bcrypt import Bcrypt
from flask import flash
from flask import render_template, redirect, request, session, jsonify
from flask_app import app
from flask_app.models.user_model import User
bcrypt = Bcrypt(app)

@app.route('/weather')
def weather():
    return render_template('weather.html')