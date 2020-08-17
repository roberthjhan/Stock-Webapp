"""
File containing web app
Author: Robert Han

http://embed.redditjs.com/
https://bytenbit.com/embed-latest-tweet-website-automatically/

To do:
- use candles to show increases or decreases in plot
"""
import os
from flask import Flask, render_template, url_for, request, flash, redirect
from form import StockForm
from chart import get_stock, chart_it, test_chart

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
        #flash(f"Invalid!", "error")
        return render_template("stonk.html", title = "Stonk lookup", form = form)

@app.route("/lookup/<ticker>/", methods = ["GET", "POST"])
def lookup(ticker):
    ''' Lookup page has a interactive Bokeh plot for the specified stock information'''
    data = get_stock(ticker, "/ytd") #buttons for ytd, 1yr, etc...
    # If no stock data received, return to /stonks and flash an error
    if "Error" in data:
        flash(f"{data}", "error")
        return redirect(url_for("stonks"))
    else:
        flash(f"Found {ticker}!", "success")
    # Generate plot elements
    script, plot_div = chart_it(data)
    plot = (script, plot_div)
    # May need new form for this
    form = StockForm()
    return render_template("lookup.html", title = ticker.upper(), form = form, plot = plot)

@app.route("/wsb")
def wsb():
    "Hold wallstreetsbets content in one page for less cringe when people look at this"
    # script, plot_div = market_sum()
    # plot = (script, plot_div)
    return render_template("wsb.html")

# run from script in debug mode
if __name__ == "__main__":
    app.run(debug = True)