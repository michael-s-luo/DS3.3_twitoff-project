from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


# User Table
class User(DB.Model):
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    # username column
    username = DB.Column(DB.String, nullable=False)
    # backref tweets
    # tweets = []

    def __repr__(self) -> str:
        return f"User: {self.username}"


# Tweets Table
class Tweet(DB.Model):
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    # text column
    text = DB.Column(DB.Unicode(300))
    # user_id column
    user_id = DB.Column(
        DB.BigInteger, DB.ForeignKey("user.id"), nullable=False
    )
    # user column: 2-way link between user & tweet with backref
    user = DB.relationship("User", backref=DB.backref("tweets", lazy=True))

    def __repr__(self) -> str:
        return f"Tweet: {self.text}"
