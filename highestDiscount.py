
def highest_discount(prod_list):
    max_discount = 0
    max_index = -1
    for i in range(len(prod_list)):
        item = prod_list[i]
        curr_discount = int(item['Discount'].strip('%'))
        max_discount = max(curr_discount, max_discount)
        if max_discount == curr_discount:
            max_index = i
    try:
        return prod_list[max_index]
    except:
        return 'No best offer found!'
