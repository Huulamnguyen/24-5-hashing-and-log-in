from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Tweet
from forms import UserForm, TweetForm
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgres:///auth_demo"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SQLALCHEMY_ECHO"] = True

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "hellodefaultsecretkey")

app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.route("/")
def home_page():
    return render_template("index.html")


# TODO: TWEETS ROUTE
@app.route("/tweets", methods=["GET", "POST"])
def show_tweets():
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect("/")
    form = TweetForm()
    all_tweets = Tweet.query.all()
    if form.validate_on_submit():
        text = form.text.data
        new_tweet = Tweet(text=text, user_id=session["user_id"])
        db.session.add(new_tweet)
        db.session.commit()
        flash("Tweet Created!", "success")
        return redirect("/tweets")

    return render_template("tweets.html", form=form, tweets=all_tweets)


# TODO: DELETE TWEET ROUTE
@app.route("/tweets/<int:id>", methods=["POST"])
def delete_tweet(id):
    """Delete tweet"""
    if "user_id" not in session:
        flash("Please login first!", "danger")
        return redirect("/login")
    tweet = Tweet.query.get_or_404(id)
    if tweet.user_id == session["user_id"]:
        db.session.delete(tweet)
        db.session.commit()
        flash("Tweet deleted!", "info")
        return redirect("/tweets")
    flash("You don't have permission to do that!", "danger")
    return redirect("/tweets")


# TODO: REGISTER ROUTE
@app.route("/register", methods=["GET", "POST"])
def register_user():
    form = UserForm()
    if form.validate_on_submit():
        # todo: get username and password from the form
        username = form.username.data
        password = form.password.data

        # todo: add new user to database
        new_user = User.register(username, password)
        db.session.add(new_user)

        # todo: because username is unique, it wil raise errors.
        # todo: this try to catch error and redirect to register form.
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("Username taken.  Please pick another")
            return render_template("register.html", form=form)

        # todo: create session to remember when user login
        session["user_id"] = new_user.id
        flash("Welcome! Successfully Created Your Account!", "success")
        return redirect("/tweets")

    return render_template("register.html", form=form)


# TODO: LOGIN ROUTE
@app.route("/login", methods=["GET", "POST"])
def login_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session["username"] = user.username
            session["user_id"] = user.id
            return redirect("/tweets")
        else:
            # todo: display errors if apply
            form.username.errors = ["Invalid username/password."]

    return render_template("login.html", form=form)


# TODO: LOG OUT ROUTE
@app.route("/logout")
def logout_user():
    # todo: remove session
    session.pop("user_id")
    flash("Goodbye!", "info")
    return redirect("/")
