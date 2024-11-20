from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.

def base_view(request):
    is_authenticated = request.user.is_authenticated
    is_admin = request.user.is_staff
    context = {
        'is_authenticated': is_authenticated,
        'is_admin': is_admin
    }
    return render(request, 'base.html', context)


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'register successful')
            return redirect('home_page')
        else:
            return render(request, "UserRegister.html", {"form": form})
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, "UserRegister.html", context)
