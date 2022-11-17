from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post
from .forms import PostForm
from django.db.models import Q

def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 9)
    

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
            "posts": page_obj,
            "paginator":paginator,
            "is_paginated" : False if paginator.num_pages == 1 else True,
            "page_obj":page_obj,
            "title":"Home",
            }

    return render(request, 'blog/index.html', context=context)


def detail(request, id):
    post = Post.objects.get(id=id)
    return render(request, 'blog/detail.html', {'post': post,"title":post.title})


def DeletePost(request, id):
    post = Post.objects.get(id=id)
    if request.user == post.author:
        post.delete()
        messages.success(request, 'Post Deleted')
    else:
        messages.warning(request, "You Don't Have Accsess")

    return redirect('post:home')

def UpdatePost(request, id):
    post = Post.objects.get(id=id)

    if request.user == post.author or request.user.is_superuser:
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES,instance=post)
            if form.is_valid:
                form.save()
                messages.success(request, 'Post Updated')

            return redirect('post:detail',id=post.id)
        elif request.method == "GET":
            form = PostForm(instance=post)
            return render(request,'blog/update.html',{"form":form,'post':post,"title":"Update Post"})
    else:
        messages.warning(request, "You Don't Have Accsess")

        return redirect('post:home') 


def search(request):
    q = request.GET.get('q')
    posts = Post.objects.filter(Q(body__icontains=q) | Q(title__icontains=q))
    paginator = Paginator(posts, 3)
    

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
            "posts": page_obj,
            "paginator":paginator,
            "is_paginated" : False if paginator.num_pages == 1 else True,
            "page_obj":page_obj,
            "q":q,
            "title":"Search"
            }

    return render(request, 'blog/index.html', context=context)