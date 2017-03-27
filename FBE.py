import feedparser
from flask import Flask
from flask import render_template
from flask import request
from flask import make_response

import json
import urllib2
import urllib
import datetime



app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640',
             'tech insider': 'http://www.businessinsider.com/sai/rss',
             'business insideri': 'http://uk.businessinsider.com/rss',
             'food network': 'http://blog.foodnetwork.com/feed/',
             'food': 'http://www.food.com/rss',
             'rollingstone': 'http://www.rollingstone.com/rss',
             'all recipes': 'http://dish.allrecipes.com/feed/',
             'hacker news' : 'https://news.ycombinator.com/rss',
             'new york times' : 'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
             'al jazeera' : 'http://www.aljazeera.com/xml/rss/all.xml',
             'the hill' : 'http://thehill.com/rss/syndicator/19110',
             'reuters' : 'http://feeds.reuters.com/reuters/USVideoBreakingviews',
             'make' : 'http://makezine.com/feed/',

# *******medium **************************************************************
             'free code camp' : 'https://medium.freecodecamp.com/feed',

             'betterhumans': 'https://betterhumans.coach.me/feed' }

DEFAULTS = {'publication':'bbc',
            'city': 'Madrid',
            'currency_from':'GBP',
            'currency_to':'USD'
            }

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=edb96feafeb8859a5416a26d06392474"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=851993723fdf4801a660745aef7880b4"

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route("/")
def home():
    # get customised headlines, based on user input or default
    publication = request.args.get("publication")
    if not publication:
        publication = request.cookies.get("publication")
        if not publication:
            publication = DEFAULTS["publication"]
    # get customized weather based on user input or default
    city = request.args.get('city')
    if not city:
        city = request.cookies.get('city')
        if not city:
            city = DEFAULTS['city']
    weather = get_weather(city)
    # get customized currency based on user input or default
    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = request.cookies.get("currency_from")
        if not currency_from:
            currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = request.cookies.get("currency_to")
        if not currency_to:
          currency_to=DEFAULTS['currency_to']
    rate, currencies = get_rate(currency_from, currency_to)
    articles = get_news(publication)

    # Cookie
    resp = make_response(render_template("home.html", articles=articles, weather=weather,
                                              currency_from=currency_from,
                                              currency_to=currency_to,
                                              rate=rate,
                                              currencies=sorted(currencies)))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    resp.set_cookie("publication", publication, expires=expires)
    resp.set_cookie("city", city, expires=expires)
    resp.set_cookie("currency_from", currency_from, expires=expires)
    resp.set_cookie("currency_to", currency_to, expires=expires)

    return resp


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(query):
    query = urllib.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {'description':parsed['weather'][0]['description'],'temperature':parsed['main']['temp'],'city':parsed['name'],"Country":parsed["sys"]["country"]}
    return weather

def get_rate(frm, to):
        all_currency = urllib2.urlopen(CURRENCY_URL).read()

        parsed = json.loads(all_currency).get('rates')
        frm_rate = parsed.get(frm.upper())
        to_rate = parsed.get(to.upper())
        return (to_rate / frm_rate, parsed.keys())



if __name__ == "__main__":
    app.run(port=5000, debug=True)
