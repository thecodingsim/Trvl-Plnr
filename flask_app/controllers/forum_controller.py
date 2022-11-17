from flask_app.models import user_model
from flask_bcrypt import Bcrypt
from flask import flash
from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.forum_model import Forum
bcrypt = Bcrypt(app)



# ============main pages================

# homepage routes to show after login and register
@app.route('/forum')
def all_posts():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    logged_user = User.get_by_id(data)
    all_posts = Forum.get_all()
    return render_template("forum.html", logged_user = logged_user, all_posts = all_posts)


# create button will route to new 
@app.route('/forum/new')
def create():
    data = {
        'id': session['user_id']
    }
    logged_user = User.get_by_id(data)
    return render_template("forum_new.html", logged_user = logged_user)

# save post when created
@app.route('/forum/save', methods=['POST'])
def save():
    print(request.form)
    if 'user_id' not in session:
        return('/')
    if not Forum.validator(request.form):
        return redirect('/forum/new')
    data = {
        **request.form,
        # utilize this to post data in posted by
        'posted_by': session['user_id'],
        'user_id': session['user_id']
        }
    Forum.save(data)
    return redirect('/forum')

# ===================SHOW CARD===========================

@app.route('/forum/<int:id>')
def show(id):
    if 'user_id' not in session:
        return('/')
    data = {
        'id': session['user_id']
    }
    logged_user = User.get_by_id(data)
    this_post = Forum.get_by_id({'id':id})
    return render_template("forum_show.html", this_post=this_post, logged_user = logged_user)

# ======================= EDIT================================

@app.route('/forum/edit/<int:id>')
def edit(id):
    # if user not logged in, you can not edit anything
    if 'user_id' not in session:
        return('/')
        # we only want to get one id to edit
    data = {
        'id': id,
        'id': session['user_id']
    }
    posts = Forum.get_by_id(data)
    logged_user = User.get_by_id(data)
    this_post = Forum.get_by_id({'id':id})
    return render_template("forum_edit.html", posts = posts, this_post=this_post, logged_user = logged_user)

@app.route('/forum/<int:id>/update', methods=['POST'])
def update(id):
    # if user not logged in, you can not update anything
    if 'user_id' not in session:
        return('/')
    if not Forum.validator(request.form):
        return redirect(f"/forum/edit/{id}")
    data = {
        'id': id,
        **request.form
    }
    Forum.update(data)
    return redirect('/forum')


# delete forum post
@app.route('/forum/<int:id>/delete')
def delete(id):
    # if user not logged in, you can not delete anything
    if 'user_id' not in session:
        return redirect('/')
    Forum.delete({'id':id})
    return redirect('/forum')