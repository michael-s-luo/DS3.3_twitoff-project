# TwitOff!

**UPDATE 2023-05**: This app uses Elevated Twitter v1.1 API, which supposedly has sunsetted in favor of v2. v2 no longer offers a free tier of access to access user tweets. Currently this app still works, but may stop at anytime.

TwitOff is a simple webapp; it compares the tweets of two Twitter users and predicts whom is more likely to tweet a hypothetical block of text. This is my first venture in combining data science and machine learning with 'productization' through deploying everything as a web app with a functional user interface.

Link: [TwitOff!](https://twitoff-m-s-luo.herokuapp.com/)

## Description

Users are able to add valid Twitter users and their most recent tweets, enter a hypothetical tweet, and generate predictions. 

This app was developed using the Flask micro-framework and is currently live/deployed on Heroku. It uses Gunicorn for the production server, a managed PostgreSQL instance via ElephantSQL to store users and their tweets, and a real-time machine learning model to generate predictions. Due to resource and memory constraints that come with Heroku, tweets are vectorized by a pretrained spaCy NLP model before being fed to train an online scikit-learn model. The model was purposefully kept simple to generate instant predictions.

## How to use

By default, tweets from Nasa, Nike, and NPR are available in TwitOff to view and make predictions. 

Reference screenshot of the homepage:
![Homepage](/screenshots/home_page.png)

* Add a Twitter handle: Twitter Users can be added on the right-hand side. Clicking their usernames will show recent tweets
* Home Page: The TwitOff! logo on the top left 
* View tweets: On the right-hand side, click on the username links
* 'Update Tweets' will fetch and sync new tweets
* 'Reset Database' will clear all users and tweets
* Make Predictions: Forms on the left allow for choosing of Twitter handles. Enter a hypothetical tweet and click 'Compare Users' to make a prediction based of their tweets!

Prediction example of Nasa vs Nike:
![Prediction](/screenshots/prediction.png)
