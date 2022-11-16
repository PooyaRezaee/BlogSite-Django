from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post


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
            }

    return render(request, 'blog/index.html', context=context)


def detail(request, id):
    post = Post.objects.get(id=id)
    return render(request, 'blog/detail.html', {'post': post})


def DeletePost(request, id):
    Post.objects.get(id=id).delete()
    messages.success(request, 'Post Deleted')

    return redirect('home')
