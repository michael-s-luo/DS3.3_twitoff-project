"""
App 'factory' for a flask instance.
Handles all the routing and browser requests for the Twitoff app using
Flask.
"""

from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import add_or_update_user
from .predict import predict_user


def create_app():

    app = Flask(__name__)

    # DB configurations, connect database & app
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    DB.init_app(app)

    @app.route("/")
    def root():
        # Query users table for the home page
        users = User.query.all()

        return render_template("base.html", title="Home", users=users)

    @app.route("/reset")
    def reset():
        # Drop all database tables
        DB.drop_all()

        # Recreate tables according to schema in models.py
        DB.create_all()

        return render_template("base.html", title="Reset Database")

    # @app.route("/populate")
    # def populate():
    #     # test two users
    #     add_or_update_user("nasa")
    #     add_or_update_user("austen")

    #     users = User.query.all()
    #     return render_template(
    #         "base.html", title="Populate Database", users=users
    #     )

    @app.route("/update")
    def update():
        users = User.query.all()

        # Get most recent tweets from each user
        for user in users:
            add_or_update_user(user.username)

        return render_template("base.html", title="Users Updated", users=users)

    @app.route("/user", methods=["POST"])
    @app.route("/user/<username>", methods=["GET"])
    def user(username: str = None, message=""):
        """Handles requests to add a new user using POST and to view a current
        user's tweets using GET.

        Parameters
        ----------
        username : str, optional
            Twitter screen_name, by default None
        message : str, optional
            optional msg to be displayed for html, by default ""

        Returns
        -------
        render_template

        """
        # If no provided user name, get username from POST request
        username = (
            username or request.values["user_name"]
        )  # user_name is defined in the html file

        try:
            if request.method == "POST":
                add_or_update_user(username)
                message = f"User {username} has been successfully added."

            tweets = User.query.filter(User.username == username).one().tweets
        except Exception as e:
            message = f"Error adding {username}: {e}"
            tweets = []

        return render_template(
            "user.html", title=username, tweets=tweets, message=message
        )

    @app.route("/compare", methods=["POST"])
    def compare():
        user0, user1 = request.values["user0"], request.values["user1"]
        tweet_text = request.values["tweet_text"]

        if user0 == user1:
            message = "Please select two different users."
        else:
            prediction = predict_user(user0, user1, tweet_text)
            message = (
                f'"{tweet_text}" is more likely to be said by {prediction}'
            )

        return render_template(
            "prediction.html", title="Prediction", message=message
        )

    return app
