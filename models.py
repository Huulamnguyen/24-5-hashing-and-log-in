from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


# TODO: conect to database, table tweets
class Tweet(db.Model):
    __tablename__ = "tweets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # todo: relationship between User and Tweet
    user = db.relationship("User", backref="tweets")


# TODO: CONNECT TO DATABASE auth_demo, table users
class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.Text, nullable=False, unique=True)

    password = db.Column(db.Text, nullable=False)

    # TODO: REGISTER METHOD, CREATE NEW USERNAME AND PASSWORD THEN STORE IT AT DATABASE
    @classmethod
    def register(cls, username, pwd):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        # * turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # * return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8)

    # TODO: AUTHENTICATE METHOD, WHEN USER INPUT PASSWORD FROM FORM AND COMPARE IT TO DATABASE
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # * return user instance
            return u
        else:
            return False
