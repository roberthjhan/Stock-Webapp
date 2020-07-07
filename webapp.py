"""
File containing web app
Author: Robert Han

http://embed.redditjs.com/
https://bytenbit.com/embed-latest-tweet-website-automatically/

To do:
- make requirements.txt
- use candles to show increases or decreases in plot
- plot is not fitting in axis and label cutoff
- implement a flash warning when an invalid ticker is used or token runs out of api calls
- lookup again nonfunctional
- custom validators?
"""

from flask import Flask, render_template, url_for, request, flash, redirect
from form import StockForm
from chart import get_stock, chart_it

app = Flask(__name__)

app.config["SECRET_KEY"] = "super secret"

@app.route("/")
@app.route("/home")
def home():
    ''' Home page'''
    return render_template("home.html")

@app.route("/about")
def about():
    ''' About page'''
    return render_template("about.html", title = "About") #pass in a title

@app.route("/stonks",  methods = ["GET", "POST"])
def stonks():
    ''' Stonk page has interface for looking up a ticker symbol
    Could use a check valid ticker method. Will probably cost additional API calls.
    '''
    form = StockForm()
    if form.validate_on_submit():
        # If the form validates redirect to lookup page.
        ticker = form.ticker.data
        return redirect(url_for("lookup", ticker = ticker))
    else:
        # Custom validator?
        #flash(f"ticker not found!", "error")
        return render_template("stonk.html", title = "Stonk lookup", form = form)

@app.route("/lookup/<ticker>/", methods = ["GET", "POST"])
def lookup(ticker):
    ''' Lookup page has a interactive Bokeh plot for the specified stock information'''
    flash(f"Found {ticker}!", "success")
    data = get_stock(ticker, "/ytd") #buttons for ytd, 1yr, etc...
    script, plot_div = chart_it(data)
    plot = (script, plot_div)
    # May need new form for this
    form = StockForm()
    if request.method == "POST":
        ticker = form.ticker.data
        return redirect(url_for("lookup", ticker = ticker))
    return render_template("lookup.html", title = ticker.upper(), form = form, plot = plot)

# run from script in debug mode
if __name__ == "__main__":
    app.run(debug = True)