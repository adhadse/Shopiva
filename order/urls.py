# order\urls.py
from django.urls import path, re_path
from . import views

app_name = "order"
urlpatterns = [
    re_path(r'^profile/$', views.profile_view, name='profilePage'),
    re_path(r'^cart/$', views.cart_view, name='cartPage'),
    re_path(r'^cartToOrderRedirect/$', views.convert_cart_to_order, name='cartToOrderRedirect'),
    re_path('^orderhistory/', views.order_history_view, name='orderHistoryPage'),
    re_path('^yourtransactions/', views.transactions_view, name='transactionsPage'),
    re_path('^yourprofile/', views.profile_view, name='profilePage'),
]