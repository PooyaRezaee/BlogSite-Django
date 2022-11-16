from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterUserForm, LoginUserForm, UpdateUserForm, CreatePostForm
from account.models import User
from post.models import Post
from datetime import datetime
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator

def regiser(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(
                cd['username'], cd['email'], cd['password'], avatar=cd['avatar'])
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.save()
            messages.success(
                request, 'user registered successfully', 'success')
            return redirect('account:login')
        else:
            messages.error(request, 'Form Not Valid', extra_tags='danger')
            return redirect('account:logout')

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
                return redirect('post:home')
            else:
                messages.error(
                    request, 'UserName or Password Is Wrong', extra_tags='danger')
                return redirect('account:login')

    else:
        form = LoginUserForm()
    return render(request, 'account/login.html', {"form": form})


def LogoutUser(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'You Logouted')
        return redirect('post:home')
    else:
        return HttpResponseForbidden()


def index(request):
    if request.user.is_authenticated:
        last_posts = Post.objects.all().order_by('-created')[:5]
        
        return render(request, 'account/dashbord.html', {'dashboard': True,'last_posts':last_posts})
    else:
        return HttpResponseForbidden()
    


def myblog(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        form = UpdateUserForm(instance=user)

        posts = Post.objects.filter(author=request.user)
        paginator = Paginator(posts, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'account/myblog.html', {'myblog': True, "form": form,"posts":page_obj})
    else:
        return HttpResponseForbidden()
    


def updateuser(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        if request.method == "POST":
            form = UpdateUserForm(data=request.POST, instance=user)
            if form.is_valid():
                form.save()

                messages.success(request, 'user updated')
                return redirect('account:myblog')
            else:
                messages.warning(request, 'Form Not Valid')
                return redirect('account:myblog')

        else:
            messages.warning(request, 'fuck out')
            return redirect('post:home')
    
    else:
        return HttpResponseForbidden()
        


def CreatePost(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CreatePostForm(request.POST, request.FILES)
            if form.is_valid():
                data_form = form.cleaned_data

                title = data_form['title']
                author = data_form['author'] if 'aothor' in data_form else request.user
                body = data_form['body']
                thumbnail = data_form['thumbnail']
                created = datetime.now()

                post = Post.objects.create(
                    title=title,
                    author=author,
                    body=body,
                    thumbnail=thumbnail,
                    created=created
                )
                post.save()

                messages.success(request, 'Post Created')
                return redirect('account:dashboard')
            else:
                print(form.cleaned_data)
                messages.warning(request, 'Form Not validate')
                return redirect('account:dashboard')

        return render(request, 'account/createpost.html', {"form": CreatePostForm()})
    
    else:
        return HttpResponseForbidden()
