""" 
Functions to query Twitter API for user & tweet information, 
vectorize tweets, and update them to local database instance.
"""

from os import getenv
import tweepy
from .models import DB, Tweet, User
import spacy

# Get API keys from .env file
key = getenv("TWITTER_API_KEY")
secret = getenv("TWITTER_API_KEY_SECRET")


# Connect to twitter API via tweepy
TWITTER_AUTH = tweepy.OAuth1UserHandler(key, secret)
TWITTER = tweepy.API(TWITTER_AUTH)

# Load nlp
nlp = spacy.load("my_model/")


def add_or_update_user(username):
    """Adds a twitter user and their most recent 200 tweets
    (excluding retweets) to the database. If user is already present in
    the database, updates db with most recent tweets.

    Parameters
    ----------
    username : str
        Twitter API screen name

    Raises
    ------
    e
        Any error will prevent user and tweets tables from being updated
    """
    try:
        twitter_user = TWITTER.get_user(screen_name=username)

        # If querying User table does not return None, then this user exists already
        # Checks if user exists in local db already, otherwise create new
        db_user = User.query.get(twitter_user.id) or User(
            id=twitter_user.id, username=(twitter_user.screen_name).lower()
        )

        # Add user to db. No effect if they already exist
        DB.session.add(db_user)

        # Get most recent tweets or new tweets (in a list)
        tweets = twitter_user.timeline(
            count=200,
            exclude_replies=True,
            include_rts=False,
            tweet_mode="extended",
            since_id=db_user.newest_tweet_id,
        )

        # update User's newest_tweet_id
        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # Add all tweets individually into Tweets table
        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet.full_text[:300])
            db_tweet = Tweet(
                id=tweet.id,
                text=tweet.full_text[:300],
                vect=tweet_vector,
                user_id=db_user.id,
            )
            DB.session.add(db_tweet)

    except Exception as e:
        print(f"Error processing {username}: {e}")
        raise e

    else:
        # Commit all changes to db
        DB.session.commit()


def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector
