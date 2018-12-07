from flask import Flask
from flask import request
from flask import render_template
from coinbase.wallet.client import Client
import mysql.connector as mc

app  = Flask(__name__)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/notenoughmoney')
def notenoughoney():
  return render_template('notenoughmoney')

@app.route('/')
def westworld_main():
    symbol = get_symbol()
    btcspotprice = get_btc_spotprice()
    ethspotprice = get_eth_spotprice()
    ltcspotprice = get_ltc_spotprice()
    return render_template('main.html',stuff=symbol, stuffb=btcspotprice,stuffe=get_eth_spotprice(),stuffl=get_ltc_spotprice())

@app.route('/graphs')

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
    elif symbol == 2:
      price = get_eth_buyprice()
    elif symbol == 3:
      price = get_ltc_buyprice()
    amount = float(price["amount"])
    # balance = balance - (amount * int(qty))
    # if balance >= amount * int(qty):
    #    balance = balance - (amount * int(qty))
    # else:   
    # action = 'buy'
    # sql_trade = 'insert into trade (qty,symbol_id,price,balance,action) values (%s, %s, %s, %s, %s)'
    # sql_pl = 'Update profit_loss Set symbol_id=%s inventory=%s Where symbol_id=%s'
    #  cursor.execute("""
    #    UPDATE tblTableName
    #    SET Year=%s, Month=%s, Day=%s, Hour=%s, Minute=%s
    #    WHERE Server=%s
    # """, (Year, Month, Day, Hour, Minute, ServerID))
    # i.e insert into orders (quantity, symbol_id) values (8000,2)
    # result_trade = connection.cursor().execute(sql_trade, (qty, symbol, amount, balance, action))
    # result_pl = connection.cursor().execute(sql_profit_loss, (qty, symbol))
    # connection.commit()
    # connection.close()
    total_price = amount * int(qty)
    if total_price <= balance:
        balance = balance - (amount * int(qty))
        action = 'buy'
        sql = 'insert into trade (qty,symbol_id,price,balance,action) values (%s, %s, %s, %s, %s)'
    # i.e insert into orders (quantity, symbol_id) values (8000,2)
        result = connection.cursor().execute(sql, (qty, symbol, amount, balance, action))
        connection.commit()
        connection.close()
    else:
        return "Not enough money"
    sql_pl = 'Update profit_loss Set symbol_id=%s inventory=%s Where symbol_id=%s'
    result_pl = connection.cursor().execute(sql_profit_loss, (qty, symbol))
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
    elif symbol == 2:
      price = get_eth_sellprice()
    elif symbol == 3:
      price = get_ltc_sellprice()
    amount = float(price["amount"])
    balance = balance + (amount * int(qty))
    action = 'sell'


    sql = 'insert into trade (qty,symbol_id,price,balance,action) values (%s, %s, %s, %s, %s)'
    # i.e insert into orders (quantity, symbol_id) values (8000,2)
    result = connection.cursor().execute(sql, (qty, symbol, amount, balance, action))
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


#def trade(side, price, current_balance):
  ## Buy = True, Sell = False
#    transaction = str(current_balance)+","+str(side)+","+str(price)
#     if side:
#        current_balance = current_balance - price
#     else:
#        current_balance = current_balance + price
#    transaction = transaction + "," + str(current_balance) + '\n'
#    ledger.write(transaction)
#    return current_balance


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

def get_balance():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("select balance from trade ORDER BY trade_id DESC LIMIT 1")
    result = cursor.fetchone()
    return float(result[0] if result else 10000)


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
    

