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
	pasteURL = "http://kuyumcu.badem.io"
	response = opener.open(pasteURL)
	page = response.read().decode('utf-8')
	parse = BeautifulSoup(page,"html.parser")
	for i in parse.find_all('h1'): # Get name
		h1 = i.text.encode('utf-8').decode()
	for buy in parse.find_all(class_="BademBuyPrice"): # Get buy price
		BuyPrice = buy.text.encode('utf-8').decode()
	for sell in parse.find_all(class_="BademSellPrice"): # Get sell price
		SellPrice = sell.text.encode('utf-8').decode()
	pasteURL = "https://portal-widgets-v3.foreks.com/symbol-summary?code=SGLD"
	response = opener.open(pasteURL)
	page = response.read().decode('utf-8')
	parse = BeautifulSoup(page,"html.parser")
	SGLD = format((float((parse.find_all('strong')[0].get_text()).replace(',','.'))), '.2f')
	SGLD_badem = float(SGLD)/100
	Binance = requests.get('https://api.binance.com/api/v1/ticker/price?symbol=NANOBTC').json()
	BinanceNANO = (Binance['price'])

	Paribu = requests.get('https://www.paribu.com/ticker').json()
	ParibuBTC = Paribu['BTC_TL']['last']

	BuyPrice_digits = float((''.join(ch for ch in BuyPrice if ch.isdigit())))/10000
	SellPrice_digits = float((''.join(ch for ch in SellPrice if ch.isdigit())))/10000
	BademTRY_buy = format(((float(BinanceNANO) * ParibuBTC * BuyPrice_digits)), '.4f')
	BademTRY_sell = format(((float(BinanceNANO) * ParibuBTC  * SellPrice_digits)), '.4f')
	return render_template('start.html', Name1=h1, BademBuyRate1=BuyPrice, BademSellRate1=SellPrice, BademBuyRateTL = BademTRY_buy, BademSellRateTL = BademTRY_sell, GoldPrice = SGLD, BademPrice = SGLD_badem)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='1337')
