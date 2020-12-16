from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from register.forms import CustomerCreationForm, CustomerChangeForm
from home.models import Customers
# Register your models here.


class CustomerAdmin(UserAdmin):
    model = Customers
    add_form = CustomerCreationForm
    form = CustomerChangeForm


#   admin.site.register(CustomerAdmin)
