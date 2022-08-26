import pandas as pd
import requests
import json

import questionary
import fire

########################################################

# lists necessary for API call

c_symbols = ['BTC', 'ETH', 'LTC', 'ADA', 'DOGE', 'XMR', 'XLM', 'XRP']
slugs = ['bitcoin', 'ethereum', 'litecoin', 'cardano', 'dogecoin', 'monero', 'stellar', 'ripple']
f_symbols = ['USD','EUR', 'GBP', 'JPY', 'CAD', 'RUB', 'KRW', 'PLN']
low_fsym = ['usd', 'eur', 'gbp', 'jpy', 'cad', 'rub', 'krw', 'pln']

value_list =  {}

# API call to generate a library with Crypto-Fiat values:

def api_call(c_symbol, low_fsym, f_symbol, slug, v):
    
    for c_sym, s in zip(c_symbol, slug):
        
        for f_sym, l_fsym in zip(f_symbol, low_fsym):
            
            api_url = f'https://api.alternative.me/v1/ticker/{s}/?convert={f_sym}'
            
            response = requests.get(api_url).json()
            
            symbol_pair = c_sym + f_sym
            
            value_list[symbol_pair] = response[0][f'price_{l_fsym}']

    for k, v in value_list.items():
        value_list[k] = float(v)

    for k, v in value_list.items():
        value_list[k] = round(v, 2)

    
api_call(c_symbols, low_fsym, f_symbols, slugs, value_list)


# User experience, select your crypto to fiat value #

selection_crypto = questionary.select(
    "Which crypto would you like to know the value of?",
    choices = [
        "BTC",
        "ETH",
        "LTC",
        "ADA",
        "DOGE",
        "XMR",
        "XLM",
        "XRP"
    ]).ask()

selection_fiat = questionary.select(
    "In which fiat would you like to see the crypto value?",
    choices = [
        "USD",
        "EUR",
        "GBP",
        "JPY",
        "CAD",
        "RUB",
        "KRW",
        "PLN"
    ]).ask()


user_input = selection_crypto + selection_fiat

symbol_dict = {'BTC':'\u20BF', 'ETH':'\u039E', 'LTC':'\u0141', 'ADA':'\u20B3', 'DOGE':'\u00D0', 'XMR':'\u0271', 'XLM':'\u002A', 'XRP': '\u2715', }

# function for output

def output(value_list, user_input, selection_crypto, selection_fiat):

    for val in value_list.keys():

        if user_input == val:

            output_data = value_list[val]

            print(f'one {selection_crypto} = {output_data} {selection_fiat}')      
   

output(value_list, user_input, selection_crypto, selection_fiat)

