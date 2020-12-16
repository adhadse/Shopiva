# home\urls.py
from django.urls import path, re_path
from home import views

app_name = "home"
urlpatterns = [
    path('', views.home_view, name='productsPage'),
    re_path('^products/', views.product_details_view, name='productDetailsPage'),
re_path('^wishlist/', views.wishlist_view, name='wishlistPage'),
]
