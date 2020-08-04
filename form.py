'''
File containing Forms
Author: Robert Han
'''

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, InputRequired, NoneOf

class StockForm(FlaskForm):
    #field(label, validators)
    ticker = StringField("Ticker", validators = [InputRequired(),
                                                 Length(min = 1, max = 5),
                                                 NoneOf(values = "~!@#$%^&*()_+`1234567890-=[]\{}|;':,./<>?)]")])
    submit = SubmitField("Lookup")
