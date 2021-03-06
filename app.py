from flask import Flask
from flask import render_template, redirect, url_for, request, abort, flash, session
app = Flask(__name__)

import json
import time
from bs4 import BeautifulSoup
import urllib.request
import requests
import threading

def price():
	global Gold, Badem, BinanceNANO, ParibuBTC
	threading.Timer(5.0, price).start()
	try:
		opener = urllib.request.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		pasteURL = "https://investing.com/currencies/gau-try"
		response = opener.open(pasteURL)
		page = response.read().decode('utf-8')
		parse = BeautifulSoup(page,"html.parser")
		for gold in parse.find_all('span', class_="pid-50655-last"):
			InputText = gold.text.encode('utf-8')
		Gold=(float(InputText))/1
		Badem = format((float(Gold)/100), '.4f')
		Binance = requests.get('https://api.binance.com/api/v1/ticker/price?symbol=NANOBTC').json()
		BinanceNANO = (Binance['price'])
		Paribu = requests.get('https://www.paribu.com/ticker').json()
		ParibuBTC = Paribu['BTC_TL']['last']
	except:
		Gold = '-'
		Badem = '-'
price()


def KuyumcuPrice():
	global Title_1, BuyPrice, SellPrice, BademTRY_buy_1, BademTRY_sell_1, BuySellRate_1
	threading.Timer(5.0, KuyumcuPrice).start()
	try:
		opener = urllib.request.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		pasteURL = "https://kuyumcu.badem.io"
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
KuyumcuPrice()

@app.route('/')
def start():
	return render_template('start.html', GoldPrice=Gold, BademPrice=Badem, Name_1=Title_1, BademBuySellRate_1=BuySellRate_1)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port='1337', threaded=True)
