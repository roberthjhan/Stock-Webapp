'''
File containing get data function and plotting function for
visualizing stock data
Author: Robert Han
'''

import requests
import numpy as np
import bokeh.plotting as bok
from bokeh.models import Band, ColumnDataSource, HoverTool
from bokeh.embed import components
import pandas as pd

ERRORS = {"1": "INVALID TICKER",
          "2": "EXCEEDED API CALLS"}

# TOKEN = "pk_f2020afa73254d8891bd5c4f6cefca2b"


def get_stock(ticker = "aapl", range = ""): # REVISE TO PASS ERROR MESSAGE
    '''
    Incomplete: Process errors
    Take a ticker and range and make an API call to the IEX cloud
    Return a stock information in json format or an error
    '''
    f = open("token.txt", "r")
    token = f.read()

    if ticker.isalpha():
        ticker = ticker.lower()
        api_url2 = "https://cloud-sse.iexapis.com/stable/stock/" + ticker + \
                       "/chart" + range + "?token=" + token
        print(api_url2)
        return requests.get(api_url2).json()
    else:
        return "1"

def validate_data(data):
    ''' Incomplete '''
    if data in ERRORS.keys():
        msg = "Error " + data + ", " + ERRORS[data]
        return msg

def chart_it(data):
    '''
    Takes a json of daily stock information and plots it
    Returns the script and div components of the plot which can
    be embedded into an html file'''
    dates = np.array([day["date"] for day in data])
    dates = pd.to_datetime((dates), format = "%Y/%m/%d")
    prices = np.array(([day["low"] for day in data], [day["high"] for day in data]))
    avg_prices = np.average(prices, axis = 0)
    close = np.array([day["close"] for day in data])
    open = np.array([day["open"] for day in data])
    volume = np.array([day["volume"] for day in data])

    # output to static HTML file
    bok.output_file("lines.html")
    # Create a source cannot pass literals and expect hovertool to work as intended
    source = ColumnDataSource(data = dict(dates = dates,
                                        avg_prices = avg_prices,
                                        close = close,
                                        open = open,
                                        volume = volume))
    # create a new plot with a title and axis labels
    p = bok.figure(x_axis_type = 'datetime',
                   x_axis_label = 'date',
                   y_axis_label = '$')
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
            "close" : "printf"
        },
        mode = "vline"))

    # Get html embeddable components
    script, div = components(p)
    return script, div

# ticker = 'aapl'
# data = get_stock(ticker, "/ytd")
# print( chart_it(data, ticker))
















