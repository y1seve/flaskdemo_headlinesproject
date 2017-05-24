import json
import urllib
import feedparser
from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

# @app.route("/")
# @app.route("/bbc")
# def bbc():
#     return get_news('bbc')

# @app.route("/cnn")
# def cnn():
#     return get_news('cnn')


@app.route("/")
def get_news():
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    weather = get_weather("Wuhan,CN")
    # first_article = feed['entries'][0]
    # return """<html>
    #     <body>
    #         <h1>Headlines </h1>
    #         <b>{0}</b> <br/>
    #         <i>{1}</i> <br/>
    #         <p>{2}</p> <br/>
    #     </body>
    #     </html>""".format(first_article.get("title"), first_article.get("published"), first_article.get("summary"))
    # return render_template("home.html")
    # return render_template("home.html", title=first_article.get("title"), published=first_article.get("published"), summary=first_article.get("summary"))
    # return render_template("home.html", article=first_article)
    return render_template("home.html", articles=feed['entries'], weather=weather)


def get_weather(query):
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=4feb58f738cdf939fa6a90a3a5d7224c'
    query = urllib.parse.quote(query)
    url = api_url.format(query)
    data = urllib.request.urlopen(url).read().decode("utf-8")
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        # python dictionary
        weather = {"description":parsed["weather"][0]["description"],"temperature":parsed["main"]["temp"],"city":parsed["name"]}
    return weather


if __name__ == "__main__":
    app.run(port=5002, debug=True)
