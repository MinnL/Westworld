
cmd=connection.cursor()
cmd.execute("select sum(total_price) from trade_record")
sum_value=cmd.fetchmany(1)
sum_value=float(sum_value[0][0])
avg_price=sum_value/remain_qty

upl_buy=(buy_price-avg_price)*inventory

rpl_buy=0

rpl_sell=(sell_price-avg_price)*quantity

upl_sell=(sell_price-avg_price)*remain_qty