from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import login
from django.contrib import messages

# Create your views here.

def home_page(request):
    return render(request, 'HomePage.html')

# """
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'register successful')
            return redirect('home_page')
        else:
            print(form.errors)
            messages.error(request, f'register failed')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, "register.html", context)
# """

"""
def register_view(request):
    if request.method is 'GET':
        form = UserRegisterForm()
    else:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'register successful')
            return redirect('home_page')
        else:
            print(form.errors)
            messages.error(request, f'register failed')
    return render(request, "register.html", {'form': form})
"""