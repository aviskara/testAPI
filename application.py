from lxml import html
import requests
from time import sleep
import time
import smtplib
import requests
import numpy as np
import tweepy
import json
import os
from dotenv import load_dotenv

from flask import Flask, redirect, request_tearing_down, url_for, request
from flask_sqlalchemy import SQLAlchemy
import twitterFunctions as tF
import amazonFunctions as aF

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    products = db.Column(db.String(120))

    # additional values for potential use, need to add them though SQL commands
    #discordNotification = db.Column(db.Boolean())
    #discordHandle = db.Column(db.String(30))

    def __repr__(self):
        return f"{self.name} - {self.products}"

class preDefItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(100), unique=False)
    amazonASIN = db.Column(db.String(20))
    amazonAvailability = db.Column(db.String(20))
    amazonPrice = db.Column(db.String(20))
    amazonQuantity = db.Column(db.Float)

    def __repr__(self):
        return f"{self.name} - {self.description} - {self.amazonASIN} - {self.amazonAvailability}"

@app.route('/')
def Index():
    return {'Hello!': "name"}

@app.route('/users')
def GetUsers():
    # returns the users in database
    users = User.query.all()
    print("in funct")
    output = []
    for user in users:
        user_data = {'name':user.name, 'products': user.products}
        output.append(user_data)

    return {"users": output}

@app.route('/users/<id>')
def get_user(id):
    # returns specific user in database
    user = User.query.get_or_404(id)
    return {"name": user.name, "products": user.products}

@app.route('/predefItems', methods=['POST', 'GET'])
def LoadPredefItems():
    if request.method == 'GET':
        # returns all items in database
        items = preDefItems.query.all()
        output = []
        for item in items:
            item_data = {'name':item.name, 'description': item.description, 'asin': item.amazonASIN,
             'availability': item.amazonAvailability, 'price': item.amazonPrice, 'stock': item.amazonQuantity}
            output.append(item_data)
        return{"item-data": output}
    
    elif request.method == 'POST':
        # get availability from amazon json reposnse
        amazonJSON = aF.GetAvailabilityJSON(request.json['asin'])
        availability = amazonJSON["stock_estimation"]["availability_message"]
        price = amazonJSON["stock_estimation"]["price"]["value"]
        quantity = amazonJSON["stock_estimation"]["stock_level"]

        # create item and load onto database
        item = preDefItems(name=request.json['name'], description=request.json['description'], 
          amazonASIN=request.json["asin"], amazonAvailability = availability, amazonPrice = price, amazonQuantity = quantity)
        db.session.add(item)
        db.session.commit()
        return{'id': item.id}

@app.route('/amazon/<id>')
def GetItemAvailability(id):
    item = preDefItems.query.get_or_404(id)
    return{'name':item.name, 'description': item.description, 'asin': item.amazonASIN,
             'availability': item.amazonAvailability, 'price': item.amazonPrice, 'stock': item.amazonQuantity}