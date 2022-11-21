from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views import View
from account.models import User
from .models import Post
from .forms import PostForm


class HomeView(View):
    template_name = 'blog/index.html'

    def get(self,request):
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
            
        return render(request,self.template_name,context=context)
class DetailView(View):
    template_name = 'blog/detail.html'

    def get(self,request,id):
        post = Post.objects.get(id=id)
        return render(request, 'blog/detail.html', {'post': post,"title":post.title})



class DeletePostView(View):
    target_url = 'post:home'

    def dispatch(self, request,*args, **kwargs):
        self.post = Post.objects.get(id=kwargs['id'])

        if request.user == self.post.author or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        
        messages.warning(request, "You Don't Have Accsess")
        return redirect(self.target_url)


    def get(self,request):
        self.post.delete()
        messages.success(request, 'Post Deleted')

        return redirect(self.target_url)

class UpdatePostView(View):
    target_url = 'post:detail'
    template_name = 'blog/update.html'
    form_class = PostForm

    def setup(self, request, *args, **kwargs):
        self.post = Post.objects.get(id=kwargs['id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request ,*args, **kwargs): # HAVE A ERROR
        if request.user == self.post.author or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        
        messages.warning(request, "You Don't Have Accsess")
        return redirect(self.target_url,id=self.post.id)
    
    def get(self,request,id):
        form = self.form_class(instance=self.post)
        context = {
                "form":form,
                'post':self.post,
                "title":"Update Post"
                }

        return render(request,self.template_name,context)
    
    def post(self,request):
        form = self.form_class(request.POST, request.FILES,instance=self.post)
        if form.is_valid:
            form.save()
            messages.success(request, 'Post Updated')
            return redirect(self.target_url,id=self.post.id)

class SearchView(View):
    template_name = 'blog/index.html'

    def get(self,request):
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

        return render(request,self.template_name ,context)

class AuthorListView(View):
    template_name = 'blog/authors.html'

    def get(self,request):
        users = User.objects.all()
        context = {
                "users":users,
                "title":"Authors"
                }

        return render(request,self.template_name,context)


class AuthorPostListView(View):
    template_name = 'blog/index.html'
    
    def get(self,request,id):
        posts = Post.objects.filter(author__id=id)
        paginator = Paginator(posts, 9)
        
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
                "posts": page_obj,
                "paginator":paginator,
                "is_paginated" : False if paginator.num_pages == 1 else True,
                "page_obj":page_obj,
                "title":'t',
                "page_author":True
                }
        
        return render(request,self.template_name,context)