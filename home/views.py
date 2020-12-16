# home/urls.py
import base64

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from home.forms import ReviewForm
from order.models import Orders, OrderItem
from home.models import Customers, Products, Ratings, Wishlist


def home_view(request):
    if request.user.is_authenticated:
        customer = request.user
        cart, created = Orders.objects.get_or_create(customer=customer, status='In Cart')
        wishlist, created = Wishlist.objects.get_or_create(customer=customer)
    else:
        cart = {'get_cartitems_quantity': 0, 'get_cart_total': 0}
        wishlist = {'get_wishlist_quantity': 0}
    products = Products.objects.all()
    attributes = [product.attributes_set.all().first() for product in products]
    prdAndAttr = zip(products, attributes)

    context = {'products': prdAndAttr, 'cart': cart, 'wishlist': wishlist}
    return render(request, 'home/home.html', context)


def product_details_view(request, *args, **kwargs):
    # TODO: USE related_items to concatenate queries
    # TODO: send reviews using AJAX (load more,etc.)
    product_id = request.GET.get("product_id")
    review_form = ReviewForm()
    if request.user.is_authenticated:
        customer = request.user
        cart, created = Orders.objects.get_or_create(customer=customer, status='In Cart')
        wishlist, created = Wishlist.objects.get_or_create(customer=customer)
        try:
            item = cart.orderitem_set.get(product=product_id)
        except OrderItem.DoesNotExist:
            item = []
    else:
        item = []
        cart = {'get_cartitems_quantity': 0, 'get_cart_total': 0}
        wishlist = {'get_wishlist_quantity': 0}

    print('>>>productName:', product_id)
    product = Products.objects.get(productID=product_id)
    attributes = product.attributes_set.all().first()
    try:
        ratings = Ratings.objects.filter(productID=product_id)
    except Ratings.DoesNotExist:
        ratings = []

    '''
        To handle the form submission
    '''
    if request.method == 'POST':
        if request.user.is_authenticated:
            review_form = ReviewForm(data=request.POST)
            if review_form.is_valid():
                review = Ratings()
                review.productID = product
                review.customer = request.user
                review.subject = review_form.cleaned_data['subject']
                review.comment = review_form.cleaned_data['comment']
                if review_form.cleaned_data['ratings'] is not None:
                    review.ratings = review_form.cleaned_data['ratings']
                else:
                    review.ratings = 0
                review.save()
                return JsonResponse({'form_saved': True})
            else:
                return JsonResponse({'form_saved': False})
    return render(request, 'home/product_details.html', {'product': product,
                                                         'attributes': attributes,
                                                         'cart': cart,
                                                         'item': item,
                                                         'ratings': ratings,
                                                         'wishlist': wishlist,
                                                         'review_form': review_form})


def wishlist_view(request):
    if request.user.is_authenticated:
        customer = request.user
        cart, created = Orders.objects.get_or_create(customer=customer, status='In Cart')
        wishlist, created = Wishlist.objects.get_or_create(customer=customer)
    else:
        cart = {'get_cartitems_quantity': 0, 'get_cart_total': 0}
        wishlist = {'get_wishlist_quantity': 0}
    context = {'wishlist':wishlist, 'cart':cart}
    return render(request, 'home/wishlist.html', context)
