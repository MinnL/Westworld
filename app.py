from flask import Flask
from flask import request
from flask import Markup
from flask import render_template
from coinbase.wallet.client import Client
import mysql.connector as mc

app  = Flask(__name__)

@app.route('/login')
def login():
  return render_template('login.html')

# @app.route('/RPL')
# def RPL():
#     return render_template('RPL.html')

# @app.route('/UPL')
# def UPL():
#     id = get_id
#     totalUPL = get_totalUPL
#     return render_template('UPL.html', x= id, y = totalUPL)
  


@app.route('/notenoughmoney')
def notenoughoney():
  return render_template('notenoughmoney.html')

@app.route('/notenoughinventory')
def notenoughinventory():
  return render_template('notenoughinventory.html')

@app.route('/')
def westworld_main():
    # connection = get_connection()
    # sql = "select * from trade order by trade_id desc"
    # result = connection.cmd_query(sql)
    # rows = connection.get_rows()
    # connection.close()
    # return render_template('ledger.html', ledgers=rows[0])
    connection = get_connection()
    sql = "select * from profit_loss"
    reseult = connection.cmd_query(sql)
    rows = connection.get_rows()
    connection.close()
    symbol = get_symbol()
    btcspotprice = get_btc_spotprice()
    ethspotprice = get_eth_spotprice()
    ltcspotprice = get_ltc_spotprice()
    return render_template('main.html',pl=rows[0],stuff=symbol, stuffb=btcspotprice,stuffe=get_eth_spotprice(),stuffl=get_ltc_spotprice())


@app.route('/ledger')
def view_ledger():
   connection = get_connection()
   sql = "select * from trade order by trade_id desc"
   result = connection.cmd_query(sql)
   rows = connection.get_rows()
   connection.close()
   return render_template('ledger.html', ledgers=rows[0])

@app.route('/ordersummary1',methods=['POST'])
def process_order1():
  connection = get_connection()
  qty = request.form['qty']
    
  symbol = request.form.get('itemOrdered',type=int)
  balance = get_balance()
  if symbol == 1:
    price = get_btc_buyprice()
    mprice = get_btc_spotprice()
  elif symbol == 2:
    price = get_eth_buyprice()
    mprice = get_eth_spotprice()
  elif symbol == 3:
    price = get_ltc_buyprice()
    mprice = get_ltc_spotprice()
  amount = float(price["amount"])
  mprice = float(mprice["amount"])
  total_price = amount * float(qty)
  if total_price <= balance:
    balance = balance - (amount * float(qty))
    action = 'buy'
    sql = 'insert into trade (qty,symbol_id,price,balance,action) values (%s, %s, %s, %s, %s)'
    result = connection.cursor().execute(sql, (qty, symbol, amount, balance, action))
    connection.commit()
  else:
    connection.close()
    return render_template('notenoughmoney.html')
    
  inventory = get_inventory(symbol)
  cvwap = get_vwap(symbol)
  vwap1 = (total_price + inventory * cvwap)/ (inventory + float(qty))
  RPL = 0
  UPL = (mprice - vwap1) * (inventory+float(qty))

 

  #for graph table
  sql_graph = 'insert into graph (symbol_id, RPL,URPL) values (%s,%s,%s)'
  result_graph = connection.cursor().execute(sql_graph, (symbol,RPL, UPL))
  connection.commit()

    #for profit_loss table
  sql_pl = 'Update profit_loss Set symbol_id= %s, inventory= inventory+%s, vwap= %s, RPL =RPL+ %s, URPL=%s  Where symbol_id=%s'
  result_pl = connection.cursor().execute(sql_pl, (symbol, qty, vwap1,RPL,UPL, symbol))
  connection.commit()
  connection.close()
  return render_template('ordersummary.html')

@app.route('/ordersummary2',methods=['POST'])
def process_order2():
    connection = get_connection()
    qty = request.form['qty']
    symbol = request.form.get('itemOrdered',type=int)
    balance = get_balance()
    if symbol == 1:
      price = get_btc_sellprice()
      mprice = get_btc_spotprice()
    elif symbol == 2:
      price = get_eth_sellprice()
      mprice = get_eth_spotprice()
    elif symbol == 3:
      price = get_ltc_sellprice()
      mprice = get_ltc_spotprice()
    


    amount = float(price["amount"])
    mprice = float(mprice["amount"])
    balance = balance + (amount * float(qty))
    action ='sell'
    sql = 'insert into trade (qty,symbol_id,price,balance,action) values (%s, %s, %s, %s, %s)'
    # i.e insert into orders (quantity, symbol_id) values (8000,2)
    result = connection.cursor().execute(sql, (qty, symbol, amount, balance, action))

   
    inventory = get_inventory(symbol)
    cvwap = get_vwap(symbol)
    RPL = (amount - cvwap) * float(qty)
    UPL = (mprice - cvwap) * (inventory - float(qty))
   
   

     #for profit_loss table
    if inventory < float(qty):
      return render_template('notenoughinventory.html')
    else:
      sql_pl = 'Update profit_loss Set symbol_id= %s, inventory= inventory-%s, RPL =RPL+ %s, URPL=%s Where symbol_id=%s'
      result_pl = connection.cursor().execute(sql_pl, (symbol, qty, RPL, UPL, symbol))
      connection.commit()
      

     #for graph table
    sql_graph = 'insert into graph (symbol_id, RPL, URPL) values (%s,%s,%s)'
    result = connection.cursor().execute(sql_graph, (symbol,RPL, UPL))
    connection.commit()

  
    connection.close()
    return render_template('ordersummary.html')


@app.route('/buy')
def buy():
    symbol = get_symbol()
    btcbuyprice = get_btc_buyprice()
    ethbuyprice = get_eth_buyprice()
    ltcbuyprice = get_ltc_buyprice()
    return render_template('buy.html',stuff=symbol, stuffb=btcbuyprice,stuffe=get_eth_buyprice(),stuffl=get_ltc_buyprice())

@app.route('/sell')
def sell():
    symbol = get_symbol()
    btcsellprice = get_btc_sellprice()
    ethsellprice = get_eth_sellprice()
    ltcsellprice = get_ltc_sellprice()
    return render_template('sell.html',stuff=symbol, stuffb=btcsellprice,stuffe=get_eth_sellprice(),stuffl=get_ltc_sellprice())



def get_connection():
    return mc.connect(user='root',
    password='',
    host='127.0.0.1',
    database='westworld',
    auth_plugin='mysql_native_password')

def get_symbol():
    connection = get_connection()
    result = connection.cmd_query("select * from symbol")
    rows = connection.get_rows()
    connection.close()
    return rows[0]

def get_balance():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("select balance from trade ORDER BY trade_id DESC LIMIT 1")
    result = cursor.fetchone()
    return float(result[0] if result else 10000)

def get_inventory(x):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("select inventory from profit_loss where symbol_id = %s", (x,))
    result = cursor.fetchone()
    return int(result[0] if result else 0)

def get_vwap(x):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("select vwap from profit_loss where symbol_id = %s", (x,))
    result = cursor.fetchone()
    return int(result[0])

# def get_id():
#     connection = get_connection()
#     result = connection.cmd_query("select symbol_id from graph")
#     rows = connection.get_rows()
#     connection.close()
#     return rows[0]

# def get_totalUPL():
#     connection = get_connection()
#     result = connection.cmd_query("SELECT graph_id,@s := @s + URPL AS cumulative FROM graph CROSS JOIN (SELECT @s := 0) AS var ORDER BY graph_id")
#     rows = connection.get_rows()
#     connection.close()
#     return rows[0]
  

# get buy price
def get_btc_buyprice():
    client = Client('apibuy', 'secretbuy')
    buy_btc = client.get_buy_price(currency_pair = 'BTC-USD')
    return buy_btc

def get_eth_buyprice():
    client = Client('apibuy', 'secretbuy')
    buy_eth = client.get_buy_price(currency_pair = 'ETH-USD')
    return buy_eth

def get_ltc_buyprice():
    client = Client('apibuy', 'secretbuy')
    buy_ltc = client.get_buy_price(currency_pair = 'LTC-USD')
    return buy_ltc

# get sell price
def get_btc_sellprice():
    client = Client('apisell', 'secretsell')
    sell_btc = client.get_sell_price(currency_pair = 'BTC-USD') 
    return sell_btc

def get_eth_sellprice():
    client = Client('apisell', 'secretsell')
    sell_eth = client.get_sell_price(currency_pair = 'ETH-USD')
    return sell_eth

def get_ltc_sellprice():
    client = Client('apisell', 'secretsell')
    sell_ltc = client.get_sell_price(currency_pair = 'LTC-USD')
    return sell_ltc

# get spot price
def get_btc_spotprice():
    client = Client('apispot', 'secretspot')
    spot_btc = client.get_spot_price(currency_pair = 'BTC-USD')
    return spot_btc

def get_eth_spotprice():
    client = Client('apispot', 'secretspot')
    spot_eth = client.get_spot_price(currency_pair = 'ETH-USD')
    return spot_eth

def get_ltc_spotprice():
    client = Client('apispot', 'secretspot')
    spot_ltc = client.get_spot_price(currency_pair = 'LTC-USD')
    return spot_ltc

if __name__ == "__main__":
  app.run(debug=True)
    

