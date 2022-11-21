from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from account.models import User
from datetime import datetime
from post.models import Post
from .forms import RegisterUserForm, LoginUserForm, UpdateUserForm, CreatePostForm


class RegisterUserView(View):
    form_class = RegisterUserForm
    template_url = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'You Registred')
            return redirect('account:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_url, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'], cd['email'], cd['password'], avatar=cd['avatar'])
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.save()
            messages.success(request, 'user registered successfully', 'success')
            return redirect('account:login')
        else:
            messages.error(request, 'Form Not Valid', extra_tags='danger')
            return redirect('post:dashboard')


class LoginUserView(View):
    form_class = LoginUserForm
    template_url = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'You logged')
            return redirect('account:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_url, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                messages.info(request, f'Welcom {data["username"]}')
                return redirect('post:home')
            else:
                messages.error(request,'UserName or Password Is Wrong', extra_tags='danger')
                return redirect('account:login')


class LogoutUserView(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You Logouted')
        return redirect('post:home')


class DashbordUserView(LoginRequiredMixin,View):
    template_url = 'account/dashbord.html'
    def get(self,request):
        last_posts = Post.objects.all().order_by('-created')[:5]
        context = {
                'dashboard': True,
                'last_posts': last_posts
                }
        
        return render(request, self.template_url, context)


class MyblogUserView(LoginRequiredMixin,View):
    form_class = UpdateUserForm
    template_url = 'account/myblog.html'

    def setup(self, request, *args, **kwargs):
        self.user_getter = User.objects.get(id=request.user.id)

        return super().setup(request, *args, **kwargs)

    def get(self,request):
        user = self.user_getter
        form = self.form_class(instance=user)

        posts = Post.objects.filter(author=request.user)
        paginator = Paginator(posts, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
                'myblog': True,
                "form": form, 
                "posts": page_obj,
                }

        return render(request, self.template_url,context)
    
    def post(self,request):
        user = self.user_getter
        form = self.form_class(data=request.POST, instance=user)
        if form.is_valid():
            form.save()

            messages.success(request, 'user updated')
            return redirect('account:myblog')
        else:
            messages.warning(request, 'Form Not Valid')
            return redirect('account:myblog')

class CreatePostView(LoginRequiredMixin,View):
    form_class = CreatePostForm
    template_url = 'account/createpost.html'

    def get(self,request):
        context = {
            "form": self.form_class()
        }
        return render(request, self.template_url,context)


    def post(self,request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            data_form = form.cleaned_data

            title = data_form['title']
            author = data_form['author'] if 'author' in data_form else request.user
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

class UsersListView(LoginRequiredMixin,View): # TODO ACCSES SUPER USER
    template_url = 'account/users.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('post:home')
    
    def get(self,request):
        users = User.objects.all()
        context = {
            'page_users': True, 'users': users
        }
        return render(request, self.template_url, context)

class DeleteUserView(LoginRequiredMixin,View): # TODO ACCSES SUPER USER
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('post:home')
    
    def get(self,request,id):
        user = User.objects.get(id=id)
        user.delete()
        messages.info(request, 'User Deleted')
        return redirect('account:users')