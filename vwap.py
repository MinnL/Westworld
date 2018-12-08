#VWAP
current_qty = 0
current_VWAP = 0
make_order = True
while make_order:
    new_qty = int(input("what's the qty?"))
    price = float(input('price:'))
    new_VWAP = (new_qty*price + current_qty*current_VWAP)/(currenty_qty+new_qty)
    print(new_VWAP)
    currenty_qty = currenty_qty + new_qty
    current_VWAP = current_VWAP + new_VWAP








