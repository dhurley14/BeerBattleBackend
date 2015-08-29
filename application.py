from flask import Flask
from flask import jsonify
from bs4 import BeautifulSoup
import requests
from Beer.Beer import Beer


# EB looks for an 'application' callable by default.
application = Flask(__name__)


@application.route('/beer/<beername>')
def display_info(beername):
    beer_obj = Beer(beername)
    # print beer_obj
    beer_advocate = beer_obj.getAdvRating()
    rate_beer = beer_obj.getRBRating()
    real_beer_name = beer_obj.getName()
    beerDict = {'beername': real_beer_name, 'beeradvocate': beer_advocate,
                'ratebeer': rate_beer}
    return jsonify(**beerDict)


@application.route('/')
def index():
    return 'Hello BeerBattle!'

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
