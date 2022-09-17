# order\models.py
from hashlib import sha1
from django.db import models
from django.db.models import Sum, F
import uuid
# from home.models import Products, Customers


class Orders(models.Model):
    STATUS = (
        ('In Cart', 'In Cart'),
        ('Order placed', 'Order placed'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Issues', 'Issues'),
        ('Cancelled', 'Cancelled'),
    )
    orderID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    customer = models.ForeignKey('home.Customers', on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=32, choices=STATUS)
    timeStamp = models.DateTimeField(auto_now_add=True)
    transactionID = models.UUIDField(max_length=200, default=None, null=True, blank=True)

    @property
    def get_order_total(self):
        # Grand sum of price of items in Order
        # REMINDER : THIS SHOULD ONLY BE CALLED ONCE THE ORDER IS DELIVERED
        # TRANSACTION IS MADE !!!
        orderItems = self.orderitem_set.all()
        total = sum([item.get_saved_orderItem_total for item in orderItems])
        return total

    @property
    def get_cart_total(self):
        # Grand sum of price of items in cart
        if self.status == 'In Cart':
            orderItems = self.orderitem_set.all()
            total = sum([item.get_total for item in orderItems])
            return total
        else:
            return 0

    @property
    def get_cartitems_quantity(self):
        # Total no of items in cart
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self):
        return 'OrderID: {} | Customer: {} '.format(str(self.orderID), str(self.customer))

    class Meta:
        verbose_name_plural = "Orders"


class OrderItem(models.Model):
    """
        This is a holder for the item in the cart/order.
    """
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey('home.Products', on_delete=models.CASCADE, null=True)
    savedProductPrice = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    timeStamp = models.DateTimeField(auto_now_add=True)

    @property
    def get_saved_orderItem_total(self):
        # return Total price of orderItem once the order's Transaction is done
        if self.savedProductPrice:
            return self.savedProductPrice * self.quantity
        else:
            return 0

    @property
    def get_total(self):
        return self.product.productPrice * self.quantity

    def __str__(self):
        return 'Product:{} | Quantity: {}'.format(self.product, self.quantity)


class ShippingAddress(models.Model):
    customer = models.ForeignKey('home.Customers', on_delete=models.SET_NULL, null=True)
    order = models.OneToOneField(Orders, primary_key=True, default=uuid.uuid4(), on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    timeStamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.address)




