from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('register/',views.regiser,name='register'),
    path('login/',views.LoginUser,name='login'),
    path('logout/',views.LogoutUser,name='logout'),
    path('',views.index,name='dashboard'),
    path('myblog/',views.myblog,name='myblog'),
    path('upusr/',views.updateuser,name='update-user'),
    path('create/post/',views.CreatePost,name='create-post'),
    path('users/',views.users,name='users'),
    path('users/delete/<int:id>',views.delete_user,name='delete-users'),
]
