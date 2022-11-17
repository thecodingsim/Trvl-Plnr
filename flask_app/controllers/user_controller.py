from flask_app.models import user_model
from flask_bcrypt import Bcrypt
from flask import flash
from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.forum_model import Forum
bcrypt = Bcrypt(app)

# main homepage, login and registration
@app.route('/')
def main():
    return render_template("homepage.html")

@app.route('/welcome')
def welcome():
    return render_template("welcome.html")


# ===============REGISTER=====================

# when user registers:
@app.route('/users/register', methods=['POST'])
def user_reg():
    if not User.validator(request.form):
        return redirect('/')
    # hash the password
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hashed_pass
    }
    user_id = User.create(data)
    session['user_id'] = user_id
    return redirect("/forum")

# login
@app.route('/users/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid credentials", "log")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid credentials", "log")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/forum')


# logout
@app.route('/users/logout')
def logout():
    del session['user_id']
# alternate way to clear session
    #session.clear()
    return redirect("/")

