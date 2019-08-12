from flask import Flask
from flask import render_template, redirect, url_for, request, abort, flash, session
app = Flask(__name__)

import json
import time
from bs4 import BeautifulSoup
import urllib.request
import requests

@app.route('/')
def start():
	opener = urllib.request.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	pasteURL = "https://portal-widgets-v3.foreks.com/symbol-summary?code=XAU/TRL"
	response = opener.open(pasteURL)
	page = response.read().decode('utf-8')
	parse = BeautifulSoup(page,"html.parser")
	Gold = format((float((parse.find_all('strong')[0].get_text()).replace('.','').replace(',','.'))/31.1034807), '.2f')
	Badem = format((float(Gold)/100), '.4f')
	Binance = requests.get('https://api.binance.com/api/v1/ticker/price?symbol=NANOBTC').json()
	BinanceNANO = (Binance['price'])
	Paribu = requests.get('https://www.paribu.com/ticker').json()
	ParibuBTC = Paribu['BTC_TL']['last']
	try:
		pasteURL = "http://kuyumcu.badem.io"
		response = opener.open(pasteURL)
		page = response.read().decode('utf-8')
		parse = BeautifulSoup(page,"html.parser")
		Title_1 = ('Kuyumcu')
		for buy in parse.find_all(class_="BademBuyPrice"): # Get buy price
			BuyPrice = buy.text.encode('utf-8').decode()
		for sell in parse.find_all(class_="BademSellPrice"): # Get sell price
			SellPrice = sell.text.encode('utf-8').decode()
		BuyPrice_digits = float((''.join(ch for ch in BuyPrice if ch.isdigit())))/10000
		SellPrice_digits = float((''.join(ch for ch in SellPrice if ch.isdigit())))/10000
		BademTRY_buy_1 = format(((float(BinanceNANO) * ParibuBTC * BuyPrice_digits)), '.4f')
		BademTRY_sell_1 = format(((float(BinanceNANO) * ParibuBTC  * SellPrice_digits)), '.4f')
		BuySellRate_1 = BuyPrice + ' / ' + SellPrice + ' (' + BademTRY_buy_1 + ' TL / ' + BademTRY_sell_1 + ' TL)'
	except:
		Title_1 = 'Kuyumcu'
		BuySellRate_1 = 'Kullanılamıyor.'
		BademTRY_buy_1 = '-'
		BademTRY_sell_1 = '-'

	return render_template('start.html', GoldPrice=Gold, BademPrice=Badem, Name_1=Title_1, BademBuySellRate_1=BuySellRate_1)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='1337')
