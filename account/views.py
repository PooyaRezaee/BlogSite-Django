from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import RegisterUserForm
# Create your views here.
def regiser(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        form.save()

        messages.success(request,'Account Registred')
        return redirect('home')

    form = RegisterUserForm()
    return render(request,'account/register.html',{"form":form})