from django import forms
from home.models import Customers
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomerCreationForm(UserCreationForm):
    userEmail = forms.CharField(label='', max_length=255,
                                widget=forms.EmailInput(attrs={'class': 'form-control',
                                                               'placeholder': 'johndoe@email.com'}))
    first_name = forms.CharField(label='', max_length=255,
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'John'}))
    last_name = forms.CharField(label='', max_length=255,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Doe'}))
    userPhone = forms.IntegerField(label='',
                                   widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                   'placeholder': '1234567809'}))
    password1 = forms.CharField(label='', strip=False,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': '****'}))
    # help_text=password_validation.password_validators_help_text_html(),)
    password2 = forms.CharField(label='', strip=False,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': '****'}))

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('userEmail', 'first_name', 'last_name', 'userPhone')


class CustomerChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = UserChangeForm.Meta.fields
