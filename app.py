from flask import Flask
from flask import request
from flask import render_template
from coinbase.wallet.client import Client
import mysql.connector as mc

app  = Flask(__name__)

@app.route('/home')
    symbol = get_symbol()
    buyprice = get_buyprice()
    sellprice = get_sellprice()
    spotprice = get_spotprice()
    initial_balance = 0
    balance = initial_balance
    return render_template('main.html')

@app.route('/ordersummary')
def view_ordersummary():
    connection = get_connection()
    sql = "select * from symbol,trade where symbol.symbol_id = trade.product_id"
    result = connection.cmd_query(sql)
    rows = connection.get_rows()
    connection.close()
    return render_template('ordersummary.html', ordersummary=rows[0])

@app.route('/graphs')

@app.route('/ledger')
def view_ledger():
    connection = get_connection()
    sql = "select * from symbol,trade where symbol.symbol_id = trade.product_id"
    result = connection.cmd_query(sql)
    rows = connection.get_rows()
    connection.close()
    return render_template('ledger.html', ledgers=rows[0])

def trade(side, price, current_balance):
  ## Buy = True, Sell = False
    transaction = str(current_balance)+","+str(side)+","+str(price)
     if side:
        current_balance = current_balance - price
     else:
        current_balance = current_balance + price
    transaction = transaction + "," + str(current_balance) + '\n'
    ledger.write(transaction)
    return current_balance

def get_connection():
    return mc.connect(user='root',
    password='jigru8MySQL',
    host='127.0.0.1',
    database='westworld',
    auth_plugin='mysql_native_password')

def get_symbol():
    connection = get_connection()
    result = connection.cmd_query("select * from symbol")
    rows = connection.get_rows()
    connection.close()
    return rows[0]

def get_buyprice():
    client = Client('apibuy', 'secretbuy')
    buy_btc = client.get_buy_price(currency_pair = 'BTC-USD')
    buy_eth = client.get_buy_price(currency_pair = 'ETH-USD')
    buy_ltc = client.get_buy_price(currency_pair = 'LTC-USD')
    return buy_btc, buy_eth, buy_ltc
    
def get_sellprice():
    client = Client('apisell', 'secretsell')
    sell_btc = client.get_sell_price(currency_pair = 'BTC-USD')
    sell_eth = client.get_sell_price(currency_pair = 'ETH-USD')
    sell_ltc = client.get_sell_price(currency_pair = 'LTC-USD')
    return sell_btc, sell_eth, sell_ltc


def get_spotprice():
    client = Client('apispot', 'secretspot')
    spot_btc = client.get_spot_price(currency_pair = 'BTC-USD')
    spot_eth = client.get_spot_price(currency_pair = 'ETH-USD')
    spot_ltc = client.get_spot_price(currency_pair = 'LTC-USD')
    return spot_btc, spot_eth, spot_ltc

    


