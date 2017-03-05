import feedparser
from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640',
             'ti': 'http://www.businessinsider.com/sai/rss',
             'bi': 'http://uk.businessinsider.com/rss',
             'fn': 'http://blog.foodnetwork.com/feed/',
             'food': 'http://www.food.com/rss',
             'med': 'https://medium.com/feed/@Medium',
             'rs': 'http://www.rollingstone.com/rss',
             'dlish': 'http://dish.allrecipes.com/feed/',
             'hn' : 'https://news.ycombinator.com/rss'}



@app.route("/")
def get_news():
        query = request.args.get("publication")
        if not query or query.lower() not in RSS_FEEDS:
                publication = "bbc"
        else:
                publication = query.lower()
        feed = feedparser.parse(RSS_FEEDS[publication])
        return render_template("home.html",articles=feed['entries'])



if __name__ == "__main__":
    app.run(port=5000, debug=True)






# kool
