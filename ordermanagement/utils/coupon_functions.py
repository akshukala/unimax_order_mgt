from DBLayer.order_management.models import Order
from DBLayer.Customer.models import BillingAddress, Farmer
from DBLayer.krishiex_app_db.models import User_data

def village_special1(farmer_id):
    order_count = Order.objects.filter(billing_address__village=BillingAddress.objects.get(farmer__farmer_id=int(farmer_id)).village).count()
    if order_count < 5:
        return True
    else:
        return False
    
def village_special2(farmer_id):
    order_count = Order.objects.filter(billing_address__village=BillingAddress.objects.get(farmer__farmer_id=int(farmer_id)).village).count()
    if order_count > 5 and order_count < 20:
        return True
    else:
        return False

def app_coupon(farmer_id):
    app_user_exists = User_data.objects.filter(mobile=Farmer.objects.get(farmer_id=int(farmer_id)).mobile_1).exists()
    if app_user_exists:
        return True
    else:
        return False
# def first_five(farmer_id):
#     order_count = Order.objects.filter(owner=Farmer.objects.get(farmer_id=int(farmer_id))).count()
#     if order_count < 5:
#         return True
#     else:
#         return False
#     
# def first_ten(farmer_id):
#     order_count = Order.objects.filter(owner=Farmer.objects.get(farmer_id=int(farmer_id))).count()
#     if order_count > 5 and order_count <30:
#         return True
#     else:
#         return False