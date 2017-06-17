from ordermanagement.core.sale_order_data_handler import SaleOrderDataHandler


def handle_request(data):
    saleorder = SaleOrderDataHandler(data)
    return saleorder.save()