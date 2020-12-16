from django.forms import ModelForm
from .models import Orders


class OrderForm():
    class Meta:
        model = Orders
