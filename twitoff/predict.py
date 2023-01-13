from sklearn.linear_model import LogisticRegression
import numpy as np
from .models import User
from .twitter import vectorize_tweet


def predict_user(user0_username, user1_username, tweet_text):

    # Get user info from database
    user0 = User.query.filter(User.username == user0_username).one()
    user1 = User.query.filter(User.username == user1_username).one()

    # Get word embeddings for each user
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # Create X_train matrix
    X_train = np.vstack([user0_vects, user1_vects])

    # Create y_target (0 for user0, 1 for user1)
    zeros = np.zeros(user0_vects.shape[0])
    ones = np.ones(user1_vects.shape[0])
    y_target = np.concatenate([zeros, ones])

    # Instantiate, fit logistic regression
    model_lr = LogisticRegression().fit(X_train, y_target)

    # Make & return prediction for hypothetical tweet text
    # return model_lr.predict([vectorize_tweet(tweet_text)])[0]

    return (
        user0_username
        if model_lr.predict([vectorize_tweet(tweet_text)])[0] == 0
        else user1_username
    )
