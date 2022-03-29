from lxml import html
import requests
from time import sleep
import time
import smtplib

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    products = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.products}"

def check(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
     
    # adding headers to show that you are
    # a browser who is sending GET request
    page = requests.get(url, headers = headers)
    for i in range(20):
        # because continuous checks in
        # milliseconds or few seconds
        # blocks your request
        sleep(3)
         
        # parsing the html content
        doc = html.fromstring(page.content)
         
        # checking availability
        XPATH_AVAILABILITY = '//div[@id ="availability"]//text()'
        RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
        AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
        return AVAILABILITY

def ReadAsin(productID):
    # Asin Id is the product Id which
    # needs to be provided by the user
    Asin = productID
    url = "http://www.amazon.com/dp/" + Asin
    print ("Processing: "+url)
    ans = check(url)
    arr = [
        'Only 1 left in stock.',
        'Only 2 left in stock.',
        'In stock.']
    if ans in arr:
        return "Available"
    return "Out of Stock"

@app.route('/')
def index():
    return {'Hello!': "name"}

@app.route('/users')
def get_users():
    users = User.query.all()

    output = []
    for user in users:
        user_data = {'name':user.name, 'products': user.products}
        output.append(user_data)

    return {"users": output}

@app.route('/users/<id>')
def get_drink(id):
    user = User.query.get_or_404(id)
    return {"name": user.name, "products": user.products, "available": ReadAsin(user.products)}

