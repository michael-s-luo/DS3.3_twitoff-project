from flask import Flask, render_template
from .models import DB, User, Tweet
from .twitter import add_or_update_user


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

    @app.route("/populate")
    def populate():
        # test two users
        add_or_update_user("nasa")
        add_or_update_user("austen")

        users = User.query.all()
        return render_template(
            "base.html", title="Populate Database", users=users
        )

    @app.route("/update")
    def update():
        users = User.query.all()

        # Get most recent tweets from each user
        for user in users:
            add_or_update_user(user.username)

        return render_template("base.html", title="Users Updated", users=users)

    return app
