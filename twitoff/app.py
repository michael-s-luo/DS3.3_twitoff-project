from flask import Flask, render_template
from .models import DB, User, Tweet


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

        return "Database reset & recreated"

    @app.route("/populate")
    def populate():
        # Test user
        michael = User(id=1, username="Michael")
        DB.session.add(michael)

        # Test tweet
        tweet1 = Tweet(id=1, text="Michael's tweet text", user=michael)
        DB.session.add(tweet1)

        # Save and commit changes
        DB.session.commit()

        return "Database populated."

    return app
