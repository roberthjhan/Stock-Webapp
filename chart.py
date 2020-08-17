'''
File containing get data function and plotting function for
visualizing stock data. This file uses Bokeh to plot data
parsed from the IEX Cloud API, a RESTful API.
Author: Robert Han
'''

import numpy as np
import bokeh.plotting as bok
import requests
from bokeh.models import Band, ColumnDataSource, HoverTool, NumeralTickFormatter
from bokeh.embed import components
import pandas as pd

ERRORS = {"400": "Invalid ticker.",
          "401": "Access restricted by key.",
          "402": "Data limited by free tier.",
          "403": "Incorrect or missing key.",
          "404": "Not found.",
          "413": "Max types.",
          "429": "Too many requests.",
          "451": "Enterprise permission required.",
          "500": "IEX Cloud system error."}

def get_stock(ticker = "aapl", range = ""):
    '''
    Take a ticker and range and make an API call to the IEX cloud
    Return a stock information in json format or an error
    '''
    f = open("s_token.txt", "r")
    token = f.read()
    ticker = ticker.lower()
    # api_url = "https://cloud-sse.iexapis.com/stable/stock/" + ticker + \
    #                "/chart" + range + "?token=" + token
    api_url = "https://sandbox.iexapis.com/stable/stock/" + ticker + \
              "/chart" + range + "?token=" + token
    try:
        # Try to return a json formatted response
        return(requests.get(api_url).json())
    except:
        # An error occurred take error code and generate an error response
        response = [n for n in str(requests.get(api_url)) if n.isdigit()]
        return report_error("".join(response))

def report_error(error):
    ''' Take error code and report the error that occured '''
    msg = "Unable to access data. Error: " + error + ". " + ERRORS[error]
    return msg

def chart_it(data):
    '''
    Takes a json of daily stock information and plots it
    Returns the script and div components of the plot which can
    be embedded into an html file'''
    # Collect data
    dates = np.array([day["date"] for day in data])
    dates = pd.to_datetime((dates), format = "%Y/%m/%d")
    prices = np.array(([day["low"] for day in data], [day["high"] for day in data]))
    avg_prices = np.average(prices, axis = 0)
    close = np.array([day["close"] for day in data])
    open = np.array([day["open"] for day in data])
    volume = np.array([day["volume"] for day in data])
    # Create a source cannot pass literals and expect hovertool to work as intended
    source = ColumnDataSource(data = dict(dates = dates,
                                        avg_prices = avg_prices,
                                        close = close,
                                        open = open,
                                        volume = volume))
    # Create a new plot with a title and axis labels
    p = bok.figure(x_axis_type = 'datetime')
    p.yaxis[0].formatter = NumeralTickFormatter(format="$0.00")
    # Add a line
    p.line(x = "dates", y = "avg_prices", line_width = 3, source = source)
    # Fill under line
    band = Band(base = 'dates',
                upper = 'avg_prices',
                source = source,
                level = 'underlay',
                fill_alpha = 0.2,
                fill_color = '#55FF88')
    p.add_layout(band)
    # Create hovertool showing date, avg_price, volume, open, and close
    p.add_tools(HoverTool(
        tooltips = [
            ('Date',    '@dates{%F}'),
            ('Price',   '$@avg_prices{0.2f}'),
            ('Volume',  '@volume{0,0}'),
            ('Open',    '$@open{0.2f}'),
            ('Close',   '$@close{0.2f}')],
        formatters = {
            "@dates": "datetime",
            "price" : "printf",
            "volume": "printf",
            "open"  : "printf",
            "close" : "printf"},
        mode = "vline"))
    # Aesthetic changes
    p.toolbar.autohide = True
    p.min_border_left = 50
    p.min_border_bottom = 50
    p.background_fill_alpha = 0
    p.border_fill_alpha = 0
    # Generate html embeddable components
    script, div = components(p)
    return script, div

def market_sum():
    '''
    Take historical performance information in json from major indexes (Dow Jones Industrial, SP500
    NASDAQ and creates a plot'''
    dji = get_stock(".dji", "/ytd")
    nasdaq = get_stock(".ndaq", "/ytd")
    sp500 = get_stock(".inx", "/ytd") #Not sure about these tickers check later before testing
    print(dji)
    # Collect dates
    dates = np.array([day["date"] for day in dji])
    dates = pd.to_datetime((dates), format = "%Y/%m/%d")

    # Filter data
    dji = np.array(([day["low"] for day in dji], [day["high"] for day in dji]))
    nasdaq = np.array(([day["low"] for day in nasdaq], [day["high"] for day in nasdaq]))
    sp500 = np.array(([day["low"] for day in sp500], [day["high"] for day in sp500]))
    # Calculate average price for each day
    dji_avg = np.average(dji, axis = 0)
    nasdaq_avg = np.average(nasdaq, axis = 0)
    sp500_avg = np.average(sp500, axis = 0)

    # Create a source, cannot pass literals and expect hovertool to work as intended
    source = ColumnDataSource(data = dict(dates = dates,
                                        dji = dji_avg,
                                        nasdaq = nasdaq_avg,
                                        sp500 = sp500_avg))
    # Create a new plot with a title and axis labels
    p = bok.figure(x_axis_type = 'datetime')
    p.yaxis[0].formatter = NumeralTickFormatter(format="$0.00")
    # Add lines
    for name, data, color in zip(["Dow Jones Industrial", "NASDAQ", "S&P500"], [dji, nasdaq, sp500], ["purple", "orange", "blue"]):
        p.line(x = "dates", y = data, line_width = 3, color = color, legend_label = name, source = source)

    p.toolbar.autohide = True
    p.min_border_left = 50
    p.min_border_bottom = 50
    p.background_fill_alpha = 0
    p.border_fill_alpha = 0
    p.show()
    # Generate html embeddable components
    # script, div = components(p)
    # return script, div

def test_chart():
    x = [1,2,3,4,5,6,7,8,9]
    y = [1,2,3,4,5,6,7,8,9]

    source = ColumnDataSource(data=dict(x=x,
                                        y=y))
    # create a new plot with a title and axis labels
    p = bok.figure(x_axis_label='x',
                   y_axis_label='y')
    # Add a line
    p.line(x="x", y="y", line_width=3, source=source)
    # Fill under line
    band = Band(base='x',
                upper='y',
                source=source,
                level='underlay',
                fill_alpha=0.2,
                fill_color='#55FF88')
    p.add_layout(band)
    # Create hovertool showing date, avg_price, volume, open, and close
    p.add_tools(HoverTool(
        tooltips=[
            ('x', '$@x{0.2f}'),
            ('y', '@y{0,0}')],
        formatters={
            "x": "printf",
            "y": "printf",
        },
        mode="vline"))

    p.toolbar.autohide = True
    p.min_border_left = 50
    p.min_border_bottom = 50
    p.background_fill_alpha = 0
    p.border_fill_alpha = 0

    # output to static HTML file in the templates folder
    bok.output_file("templates/plot.html")
    bok.save(p)
    # Get html embeddable components
    script, div = components(p)
    return script, div



def test():
    market_sum()