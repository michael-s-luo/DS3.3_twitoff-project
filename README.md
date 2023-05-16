# TwitOff!

TwitOff is a simple webapp; it compares the tweets of two Twitter users and predicts whom is more likely to have tweeted a hypothetical block of text. This is my first venture in combining data science and machine learning with 'productization' through deploying everything as a web app with a functional user interface.

## Description

Users are able to add valid Twitter users and their most recent tweets, enter a hypothetical tweet, and generate predictions. 

This app was developed using the Flask micro-framework and is currently live/deployed on Heroku. It uses Gunicorn for the production server, a managed PostgreSQL instance via ElephantSQL to store users and their tweets, and a real-time machine learning model to generate predictions. Due to resource and memory constraints that come with a Heroku, tweets are vectorized by a pretrained spaCy NLP model before being fed to train an online scikit-learn model. This model was kept simple purposefully to be able to generate instant predictions.

## How to use
![test](/screenshots/prediction.png)
