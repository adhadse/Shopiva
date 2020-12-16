from django.db.models import F
from django.shortcuts import render, redirect

from .models import *
from home.models import *


def cart_view(request):
    """
        cart: cart with status = 'In Cart'
        items: items in cart
    """
    if request.user.is_authenticated:
        customer = request.user
        cart, created = Orders.objects.get_or_create(customer=customer, status='In Cart')
        items = cart.orderitem_set.all()
        wishlist, created = Wishlist.objects.get_or_create(customer=customer)
    else:
        items = []
        cart = {'get_cartitems_quantity': 0, 'get_cart_total': 0}
        wishlist = {'get_wishlist_quantity': 0}
    context = {'items': items, 'wishlist': wishlist, 'cart': cart}
    return render(request, 'order/cart.html', context)


def profile_view(request):
    if request.user.is_authenticated:
        customer = request.user
        cart, created = Orders.objects.get_or_create(customer=customer, status='In Cart')
        wishlist, created = Wishlist.objects.get_or_create(customer=customer)
    else:
        cart = {'get_cartitems_quantity': 0, 'get_cart_total': 0}
        wishlist = {'get_wishlist_quantity': 0}
    context = {'cart': cart,'wishlist':wishlist}
    return render(request, 'order/profilebase.html', context)


def convert_cart_to_order(request):
    if request.user.is_authenticated:
        customer = request.user
        try:
            # find the cart
            cart = Orders.objects.get(customer=customer, status='In Cart')
            print(cart)
            cart.status = 'Delivered'

            # TODO: BULK SAVE THE PRODUCT PRICE FOR ALL CART ITEMS
            # TODO: REUSE CODE BY USING FUNCTION
            # cart.orderitem_set.all().update(savedProductPrice = F(''))
            for cartItem in cart.orderitem_set.all().iterator():
                print(cartItem.product.productPrice)
                cartItem.savedProductPrice = cartItem.product.productPrice
                cartItem.save()

            cart.transactionID = uuid.uuid4()
            cart.save()
        except Orders.DoesNotExist:
            return redirect('home:productsPage')
    else:
        return redirect('home:productsPage')
    return redirect('order:orderHistoryPage')


def order_history_view(request):
    if request.user.is_authenticated:
        '''
            cart:   To show on navbar. order.get_item_quantity
            orders: To show in order history side content
            items:  Items per order
            order_and_items: zipped order and items
        '''
        customer = request.user
        wishlist, created = Wishlist.objects.get_or_create(customer=customer)

        try:
            # First try for any order history
            orders = Orders.objects.filter(customer=customer, status='Delivered').order_by('-timeStamp')
        except Orders.DoesNotExist:
            # No orders Yet
            orders = []

        try:
            # Then try for items in cart
            cart = Orders.objects.get(customer=customer, status='In Cart')
        except Orders.DoesNotExist:
            # No items in cart
            cart = {'get_cartitems_quantity': 0, 'get_cart_total': 0}

        # print('-----------\nORDERS: ', orders)
        # print('Items: ', items)
        # print('CART: ', cart)

        context = {'cart': cart,'wishlist':wishlist, 'orders': orders}
        return render(request, 'order/orderhistory.html', context)
    else:
        # If user is Anonymous
        orders = []
        cart = {'get_cartitems_quantity': 0, 'get_cart_total': 0}
        wishlist = {'get_wishlist_quantity': 0}
        context = {'cart': cart,'wishlist': wishlist, 'orders': orders}
        return render(request, 'order/orderhistory.html', context)


def transactions_view(request):
    if request.user.is_authenticated:
        customer = request.user
        wishlist, created = Wishlist.objects.get_or_create(customer=customer)
        try:
            # First try for any order history
            orders = Orders.objects.filter(customer=customer, status='Delivered').order_by('-timeStamp')
        except Orders.DoesNotExist:
            # No orders Yet
            orders = []

        try:
            # Then try for items in cart
            cart = Orders.objects.get(customer=customer, status='In Cart')
        except Orders.DoesNotExist:
            # No items in cart
            cart = {'get_cartitems_quantity': 0, 'get_cart_total': 0}

        # print('-----------\nORDERS: ', orders)
        # print('Items: ', items)
        # print('CART: ', cart)

        context = {'cart': cart,'wishlist':wishlist, 'orders': orders}
        return render(request, 'order/transctions.html', context)
    else:
        # If user is Anonymous
        orders = []
        cart = {'get_cartitems_quantity': 0, 'get_cart_total': 0}
        wishlist = {'get_wishlist_quantity': 0}
        context = {'cart': cart, 'wishlist': wishlist, 'orders': orders}
    return render(request, 'order/transctions.html', context)
