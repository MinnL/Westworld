def insert_value():
    connection = get_commection()
    cursor = connection.cursor()

    sql = "insert into "

    symbol_id
    inventory
    WVAP
    RPL
    URPL






sql_buy1 = ("select sum(qty) from trade where symbol_id = 1 and action = 'buy'")
result = connection.cmd.query(sql_buy1)
total_buy = connection.get_rows()
total_buy = int(total_buy[0][0][0]) + int(qty)

sql_sell1 = ("select sum(quantity) from trade where symbol_id = 1 and action = 'sell'")
result = connection.cmd.query(sql_sell1)
total_sell = connection.get_rows()
total_sell = int(total_sell[0][0][0]) + int(qty)

inventory = total_buy - total_sell



if symbol == 1:
      price = get_btc_buyprice()  
elif symbol == 2:
      price = get_eth_buyprice()
elif symbol == 3:
      price = get_ltc_buyprice()
    amount = float(price["amount"])



  # sql_buy1 = ("select sum(qty) from trade where symbol_id = 1 and action = 'buy'")
    # result = connection.cmd_query(sql_buy1)
    # total_buy = connection.get_rows()
    # total_buy = int(total_buy[0][0][0]) + int(qty)

    # sql_sell1 = ("select sum(qty) from trade where symbol_id = 1 and action = 'sell'")
    # result = connection.cmd_query(sql_sell1)
    # total_sell = connection.get_rows()
    # total_sell = int(total_sell[0][0][0]) + int(qty)

    # sql_buy2 = ("select sum(qty) from trade where symbol_id = 2 and action = 'buy'")
    # result = connection.cmd_query(sql_buy2)
    # total_buy = connection.get_rows()
    # total_buy = int(total_buy[0][0][0]) + int(qty)

    # sql_sell2 = ("select sum(qty) from trade where symbol_id = 1 and action = 'sell'")
    # result = connection.cmd_query(sql_sell2)
    # total_sell = connection.get_rows()
    # total_sell = int(total_sell[0][0][0]) + int(qty)

    sql_buy3 = ("select sum(qty) from trade where symbol_id = 3 and)
    result = connection.cmd_query(sql_buy3)
    total_buy = connection.get_rows()
    total_buy = int(total_buy[0][0][0]) + int(qty)

    inventory = total_buy - total_sell

    inventory = str(inventory)

    