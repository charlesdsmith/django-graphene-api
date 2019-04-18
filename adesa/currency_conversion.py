# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 17:56:54 2019

@author: Visitor
"""

import requests
from forex_python.converter import CurrencyRates

def get_conversion():
    try:
        c = CurrencyRates()
        current_rate = c.get_rate('USD', 'CAD')
    except:
        # Where USD is the base currency you want to use
        url = 'https://api.exchangerate-api.com/v4/latest/USD'
        
        # Making our request
        response = requests.get(url)
        data = response.json()
        current_rate = data['rates']['CAD']
    return float(current_rate)
