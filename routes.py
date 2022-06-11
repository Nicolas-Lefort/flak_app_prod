from flask import render_template, flash, redirect, url_for, session, logging, request
from app import app
from models import db, Articles, Users
from forms import RegisterForm, ArticleForm
from passlib.hash import sha256_crypt
from functools import wraps
from routes import *


# Index
@app.route('/', methods=["GET", "POST"])
def index():
    form = RegisterForm(request.form)
    if request.method == "POST" :
        # get form fields
        username = request.form["username"]
        password_candidate = request.form["password"]
        user = Users.query.filter_by(username=username).all()
        print(username, password_candidate)
        if len(user) > 0:
            # keep first record
            user = Users.query.filter_by(username=username).first()
            # get password
            password = user.password
            # compare password
            if sha256_crypt.verify(password_candidate, password):
                session["logged_in"] = True
                session["username"] = username

                flash("you are now logged in", "success")
                return redirect(url_for("dashboard"))
            else:
                error = "Invalid login"
                return render_template("home.html", error=error)

        else:
            error = "Username not found"
            return render_template("home.html", error=error)

    return render_template('home.html', form=form)

# About
@app.route('/about')
def about():
    return render_template('about.html')

# Articles
@app.route('/articles')
def articles():
    # execute query
    articles = Articles.query.all()

    if len(articles) > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = "No article Found"
        return render_template('articles.html', msg=msg)

# Single article
@app.route('/article/<string:id>/')
def article(id):
    # execute query
    article = Articles.query.get(id)

    return render_template('article.html', article=article)


# User regiser
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create object
        user = Users(name, email, username, password)

        # add user
        db.session.add(user)
        db.session.commit()
        flash("you are now logged in", "success")

        return redirect(url_for("dashboard"))

    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=["GET", "POST"])
def login():
    return redirect(url_for("index"))

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('index'))
    return wrap

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash("you are now logged out", "success")
    return redirect(url_for("index"))

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    articles = Articles.query.all()

    if len(articles) > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = "No article Found"
        return render_template('dashboard.html', msg=msg)

# Add article
@app.route('/add_article', methods=["GET", "POST"])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        body = form.body.data

        # Create object
        article = Articles(title, session["username"], body)
        db.session.add(article)
        db.session.commit()

        flash("Article created", "success")

        return redirect(url_for("dashboard"))

    return render_template('add_article.html', form=form)


# Add article
@app.route('/edit_article/<string:id>/', methods=["GET", "POST"])
@is_logged_in
def edit_article(id):
    # get article
    article = Articles.query.get(id)

    form = ArticleForm(request.form)

    # Populate article form fields
    form.title.data = article.title
    form.body.data = article.body

    if request.method == "POST" and form.validate():
        title = request.form["title"]
        body = request.form["body"]

        article.title = title
        article.body = body
        db.session.commit()

        flash("Article updated", "success")

        return redirect(url_for("dashboard"))

    return render_template('edit_article.html', form=form)

# Add article
@app.route('/delete_article/<string:id>/', methods=["POST"])
@is_logged_in
def delete_article(id):
    db.session.delete(Articles.query.get(id))
    db.session.commit()
    
    flash("Article deleted", "success")

    return redirect(url_for("dashboard"))