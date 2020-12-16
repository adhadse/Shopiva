# register\urls.py
from django.urls import path, re_path
from register import views

app_name = "register"
urlpatterns = [
    path('', views.signup_view, name='loginPage'),
    path('signin/', views.signin_view, name='signinPage'),
    path('logout/', views.logout_view, name='logoutPage'),
]

