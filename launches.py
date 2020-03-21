#! /bin/python3
'''`launches` module gets rocket launch data from SpaceX API.'''
from json import loads
from requests import get
from flask import Flask
from flask import render_template


APP = Flask(__name__)  # create Flask instance
APP.config.from_envvar('LAUNCHES_DEV_ENV')  # set environmental variable


@APP.route('/')  # route decorator
def index():
    '''`index()` method gets rocket launch data from the SpaceX API. \
And renders template for browser display.'''
    res = get("https://api.spacexdata.com/v3/launches")  # get data from API
    data = loads(res.text)  # load data
    return render_template("launches.html", data=data)  # render template


if __name__ == '__main__':
    APP.run()  # if standalone
