"""
File containing web app
Author: Robert Han

http://embed.redditjs.com/
https://bytenbit.com/embed-latest-tweet-website-automatically/

To do:
- When running make sure working directory correct
"""
from flask import Flask, render_template, url_for, flash, redirect
from form import StockForm
from chart import get_stock, chart_it, market_sum

app = Flask(__name__)
app.config["SECRET_KEY"] = "super secret"

@app.route("/")
@app.route("/home")
def home():
    ''' Home page market summary going here'''
    # Generate plot elements
    script, plot_div = market_sum()
    plot = (script, plot_div)
    return render_template("home.html", plot = plot)

@app.route("/about")
def about():
    ''' About page'''
    return render_template("about.html", title = "About")

@app.route("/stocks",  methods = ["GET", "POST"])
def stocks():
    ''' Stonk page has interface for looking up a ticker symbol'''
    form = StockForm()
    if form.validate_on_submit():
        # If the form validates redirect to lookup page.
        ticker = form.ticker.data
        return redirect(url_for("lookup", ticker = ticker))
    else:
        return render_template("stocks.html", title = "Stock lookup", form = form)

@app.route("/lookup/<ticker>/", methods = ["GET", "POST"])
def lookup(ticker):
    ''' Lookup page has a interactive Bokeh plot for the specified stock information'''
    data = get_stock(ticker, "ytd") #buttons for ytd, 1yr, etc...
    # If no stock data received, return to /stocks and flash an error
    if "Error" in data:
        flash(f"{data}", "error")
        return redirect(url_for("stocks"))
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
    "Hold wallstreetsbets content in one page"
    return render_template("wsb.html")

# run from script in debug mode
if __name__ == "__main__":
    app.run(debug = True)