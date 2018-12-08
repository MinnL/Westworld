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
    total_price = amount * int(qty)




    if qty <= inventory:
        balance = balance + (amount * int(qty))
        action = 'sell'
        sql = 'insert into trade (qty,symbol_id,price,balance,action) values (%s, %s, %s, %s, %s)'
        result = connection.cursor().execute(sql, (qty, symbol, amount, balance, action))
         connection.commit()
    else:
      connection.close()
      return render_template('notenoughmoney.html')
    sql_pl = 'Update profit_loss Set symbol_id= %s, inventory= inventory+%s Where symbol_id=%s'
    result_pl = connection.cursor().execute(sql_pl, (symbol, -qty, symbol))
    connection.commit()
    connection.close()
    return render_template('ordersummary.html')

    sql = 'insert into trade (qty,symbol_id,price,balance,action) values (%s, %s, %s, %s, %s)'
    # i.e insert into orders (quantity, symbol_id) values (8000,2)
    result = connection.cursor().execute(sql, (qty, symbol, amount, balance, action))
    connection.commit()
    connection.close()
    return render_template('ordersummary.html')

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
    total_price = amount * int(qty)
    
    
    if total_price <= balance:
      balance = balance - (amount * int(qty))
      action = 'buy'
      sql = 'insert into trade (qty,symbol_id,price,balance,action) values (%s, %s, %s, %s, %s)'
      result = connection.cursor().execute(sql, (qty, symbol, amount, balance, action))
      connection.commit()
    else:
      connection.close()
      return render_template('notenoughmoney.html')
    sql_pl = 'Update profit_loss Set symbol_id= %s, inventory= inventory+%s Where symbol_id=%s'
    result_pl = connection.cursor().execute(sql_pl, (symbol, qty, symbol))
    connection.commit()
    connection.close()
    return render_template('ordersummary.html')