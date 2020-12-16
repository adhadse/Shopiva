# serverapi\view.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

from home.forms import ReviewForm
from .serializers import OrdersSerializer
import pickle
import json
import numpy as np

from home.models import Customers, Products, Ratings, Wishlist
from order.models import Orders, OrderItem


# Create your views here.
# decorator does it that it checks the API request
# method to see if it’s a GET request being made,
# if it’s not a GET request then you won’t be able to access this function.
@api_view(['GET'])
def index_page(request):
    return_data = {
        "error": "0",
        "message": "Successful",
    }
    return Response(return_data)


# 25-31 collect data from the API endpoint and stores it in a variable
@api_view(["POST"])
def predict_diabetictype(request):
    try:
        age = request.data.get('age', None)
        bs_fast = request.data.get('bs_fast', None)
        bs_pp = request.data.get('bs_pp', None)
        plasma_r = request.data.get('plasma_r', None)
        plasma_f = request.data.get('plasma_f', None)
        hbA1c = request.data.get('hbA1c', None)
        fields = [age, bs_fast, bs_pp, plasma_r, plasma_f, hbA1c]
        if not None in fields:
            # Data preprocessing Convert the values to float
            age = float(age)
            bs_fast = float(bs_fast)
            bs_pp = float(bs_pp)
            plasma_r = float(plasma_r)
            plasma_f = float(plasma_f)
            hbA1c = float(hbA1c)
            result = [age, bs_fast, bs_pp, plasma_r, plasma_f, hbA1c]

            # Passing data to model & loading the model from disks
            model_path = 'ml_model/model.pkl'
            classifier = pickle.load(open(model_path, 'rb'))
            prediction = classifier.predict([result])[0]
            conf_score = np.max(classifier.predict_proba([result])) * 100
            predictions = {
                'error': '0',
                'message': 'Successful',
                'prediction': prediction,
                'confidence_score': conf_score
            }
        else:
            predictions = {
                'error': '1',
                'message': 'Invalid Parameters'
            }
    except Exception as e:
        predictions = {
            'error': '2',
            "message": str(e)
        }

    return Response(predictions)


@api_view(['PUT'])
def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    print('ProductID:', productID)
    print('Action:   ', action)

    if request.user.is_authenticated:
        customer = request.user
        product = Products.objects.get(productID=productID)
        cart, created = Orders.objects.get_or_create(customer=customer, status='In Cart')
        cartItem, created = OrderItem.objects.get_or_create(order=cart, product=product)

        if action == 'add':
            cartItem.quantity = cartItem.quantity + 1
            cartItem.save()
            return JsonResponse({'Deleted': False,
                                 'cartItemTotal': cartItem.get_total,
                                 'cartItemQuantity': cartItem.quantity,
                                 'cartQuantity': cart.get_cartitems_quantity,
                                 'cartTotal': cart.get_cart_total})
        elif action == 'remove':
            cartItem.quantity = cartItem.quantity - 1
            if cartItem.quantity <= 0:
                cartItem.delete()
                return JsonResponse({'Deleted': True,
                                     'cartItemTotal': cartItem.get_total,
                                     'cartItemQuantity': cartItem.quantity,
                                     'cartQuantity': cart.get_cartitems_quantity,
                                     'cartTotal': cart.get_cart_total})
            else:
                cartItem.save()
                return JsonResponse({'Deleted': False,
                                     'cartItemTotal': cartItem.get_total,
                                     'cartItemQuantity': cartItem.quantity,
                                     'cartQuantity': cart.get_cartitems_quantity,
                                     'cartTotal': cart.get_cart_total})
        elif action == 'delete':
            cartItem.quantity = 0
            cartItem.delete()
            return JsonResponse({'Deleted': True,
                                 'cartItemTotal': cartItem.get_total,
                                 'cartItemQuantity': cartItem.quantity,
                                 'cartQuantity': cart.get_cartitems_quantity,
                                 'cartTotal': cart.get_cart_total})
        elif int(action):
            cartItem.quantity = action
            cartItem.save()
            return JsonResponse({'Deleted': False,
                                 'cartItemTotal': cartItem.get_total,
                                 'cartItemQuantity': cartItem.quantity,
                                 'cartQuantity': cart.get_cartitems_quantity,
                                 'cartTotal': cart.get_cart_total})
        cartItem.save()

        if cartItem.quantity <= 0:
            cartItem.delete()

        return Response('Item was added')


@api_view(['GET'])
def orders(request):
    orders = Orders.objects.all()
    serializer = OrdersSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def updateWishlist(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    print('ProductID:', productID)
    print('Action:   ', action)

    if request.user.is_authenticated:
        customer = request.user
        wishList, created = Wishlist.objects.get_or_create(customer=customer)

        if action == 'add':
            wishList.add_item(productID)
            return JsonResponse({'wishlistItemQuantity': wishList.get_wishlist_quantity})

        elif action == 'delete':
            wishList.delete_item(productID)
            return JsonResponse({'deleted': True,
                                 'wishlistItemQuantity': wishList.get_wishlist_quantity})

        elif action == 'add_to_cart':
            return JsonResponse({'cartItemQuantity': wishList.add_to_cart(productID),
                                'wishlistItemQuantity': wishList.get_wishlist_quantity})

