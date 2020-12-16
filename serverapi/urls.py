# serverapi\urls.py
from django.urls import path
from serverapi import views

urlpatterns = [
    path('', views.index_page),
    path('orders/', views.orders, name='order'),
    path('update_item/', views.updateItem, name='updateItem'),
    path('update_wishlist/', views.updateWishlist, name='updateWishlist'),
    path('predict/', views.predict_diabetictype),
]
