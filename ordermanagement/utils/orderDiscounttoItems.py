from uni_db.order_management.models import Order, OrderItem


def getTotalSellingPrice(order):
    # return int(order.grand_total) + int(order.total_discount)
    return int(order.grand_total) + int(order.order_discount)


def getItemToUpdateDiscount(oitems):
    for oi in oitems:
        if oi.quantity == 1 and oi.selling_price != 0:
            return oi
    #return oitems[0]
    #split order items
    oi = oitems[0]
    new_oi = OrderItem()
    new_oi.order = oi.order
    
    new_oi.created_on = oi.created_on
    new_oi.updated_on = oi.updated_on
    new_oi.item_name = oi.item_name
    
    new_oi.status_code = oi.status_code
    new_oi.quantity = 1
#     new_oi.cancellable = oi.cancellable
    new_oi.selling_price = oi.selling_price
    new_oi.list_price = oi.list_price
    new_oi.discount = oi.discount
    new_oi.adj_discount = oi.adj_discount
    new_oi.prepaid_amount = oi.prepaid_amount
#     new_oi.on_hold = oi.on_hold
#     new_oi.facility_code = oi.facility_code
    new_oi.total_price = 0
    new_oi.save()
    new_oi.total_price = (new_oi.selling_price - new_oi.discount) * new_oi.quantity
    new_oi.save()
    oi.quantity = oi.quantity - 1
    oi.save()
    oi.total_price = (oi.selling_price - oi.discount) * oi.quantity
    oi.save()
    return new_oi


def updateAdvancedAmount(order):
    adv_payment = int(order.advance_payment)
    for oi in OrderItem.objects.filter(order=order):
        if adv_payment > 0:
            if oi.total_price > adv_payment:
                prepaid = adv_payment
                adv_payment = 0
            else:
                prepaid = oi.total_price
                adv_payment = adv_payment - prepaid
            oi.prepaid_amount = prepaid / oi.quantity
            oi.save()


def updateDiscounts(order):
    total_selling_price = getTotalSellingPrice(order)
    # percent = order.total_discount / float(total_selling_price)
    percent = order.order_discount / float(total_selling_price)
    total_dis_given = 0

    oitems = OrderItem.objects.filter(order=order)

    for oi in oitems:
        dis = int(((oi.selling_price - oi.discount) * percent) + 0.5)
        total_dis_given = total_dis_given + (dis * oi.quantity)
        # oi.discount = dis
        oi.adj_discount = dis
        # oi.total_price = (oi.selling_price - dis) * oi.quantity
        oi.save()

    if total_dis_given != int(order.order_discount):
        print total_dis_given
        print order.total_discount
        oi = getItemToUpdateDiscount(oitems)
        # oi.discount = oi.discount - ((total_dis_given -
        #                       int(order.total_discount)) / oi.quantity)
        # oi.total_price = (oi.selling_price - oi.discount) * oi.quantity
        oi.adj_discount = oi.adj_discount - (
            (total_dis_given - int(order.order_discount)) / oi.quantity)
        oi.save()



def updateOrderDiscountToItems(order):
    if order.order_discount > 0:
        updateDiscounts(order)
        return "Updated Discounts Successfully !"

def hold_neg_disc_order(order):
    items = OrderItem.objects.filter(order=order)
    for i in items:
        if i.adj_discount < 0 or i.prepaid_amount < 0:
            #order.unicommerce_status = "NEG_DISC_PREPAID"
            order.save()
            return


if __name__ == "__main__":
    import sys
    import django
    django.setup()
    o = Order.objects.get(sales_order_id = sys.argv[1])
    updateOrderDiscountToItems(o)
