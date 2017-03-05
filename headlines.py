import feedparser
from flask import Flask
from flask import render_template


app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640',
             'hn' : 'https://news.ycombinator.com/rss'}






@app.route("/")
@app.route("/<publication>")
def get_news(publication="hn"):
  feed = feedparser.parse(RSS_FEEDS[publication])
  return render_template("home.html", articles=feed['entries'])





if __name__ == '__main__':
  app.run(port=5000, debug=True)
