from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterUserForm, LoginUserForm
from account.models import User

# Create your views here.


def regiser(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(
                cd['username'], cd['email'], cd['password'],avatar=cd['avatar'])
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.save()
            messages.success(
                request, 'user registered successfully', 'success')
            return redirect('login')
        else:
            messages.error(request, 'Form Not Valid', extra_tags='danger')
            return redirect('logout')

        # messages.success(request, 'Account Registred')
        # return redirect('login')

    form = RegisterUserForm()
    return render(request, 'account/register.html', {"form": form})


def LoginUser(request):
    if request.method == "POST":
        form = LoginUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                messages.info(request, f'Welcom {data["username"]}')
                return redirect('home')
            else:
                messages.error(
                    request, 'UserName or Password Is Wrong', extra_tags='danger')
                return redirect('login')

    else:
        form = LoginUserForm()
    return render(request, 'account/login.html', {"form": form})


def LogoutUser(request):
    logout(request)
    messages.info(request, 'You Logouted')
    return redirect('home')
