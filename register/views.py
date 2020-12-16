from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template import RequestContext

from home.models import Customers
from django.contrib.auth import login, authenticate, logout
from .forms import CustomerCreationForm


# class SignUpView(CreateView):
#    model = Customers
#    form_class = CreateCustomerForm
#    success_url = pass
#    template_name = pass

def signup_view(request):
    # TODO: USE FORM VALIDATION ERROR TAKING EG. FROM OXOTUBE
    signup_form = CustomerCreationForm()
    if request.method == 'POST':
            signup_form = CustomerCreationForm(data=request.POST)
            if signup_form.is_valid():
                print('form valid')
                signup_form.save()
                '''
                    If successfully created account let the user sign in
                '''
                signup_form = CustomerCreationForm()
                context = {'signup_form': signup_form, 'requires_signin': True}
                return render(request, 'register/login.html', context)
            else:
                print('invalid form')
                return redirect('register:loginPage')
    context = {'signup_form': signup_form, 'requires_signin': False}
    return render(request, 'register/login.html', context)


def signin_view(request):
    if request.method == 'POST':
        print("inside sign in")
        userEmail = request.POST['userEmail']
        password = request.POST['password']
        user = authenticate(request, userEmail = userEmail, password = password)
        if user is not None:
            login(request, user)
            return redirect('home:productsPage')
        else:
            return HttpResponse("Invalid Password or Email Address", request)


def logout_view(request):
    logout(request)
    return redirect('home:productsPage')