from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post
from .forms import PostForm

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
    post = Post.objects.get(id=id)
    if request.user == post.author:
        post.delete()
        messages.success(request, 'Post Deleted')
    else:
        messages.warning(request, "You Don't Have Accsess")

    return redirect('home')

def UpdatePost(request, id):
    post = Post.objects.get(id=id)

    if request.user == post.author:
        if request.method == "POST":
            form = PostForm(request.POST,instance=post)
            if form.is_valid:
                form.save()
                messages.success(request, 'Post Updated')

            return redirect('detail',id=post.id)
        elif request.method == "GET":
            form = PostForm(instance=post)
            return render(request,'blog/update.html',{"form":form,'post':post})
    else:
        messages.warning(request, "You Don't Have Accsess")

        return redirect('home') 
