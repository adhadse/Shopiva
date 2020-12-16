from django.contrib import admin
from order.models import *


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('orderID', 'customer', 'status', 'get_cart_total', 'get_cartitems_quantity', 'get_order_total', 'timeStamp', 'transactionID')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'savedProductPrice', 'timeStamp')


admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress)