from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('register/',views.RegisterUserView.as_view(),name='register'),
    path('login/',views.LoginUserView.as_view(),name='login'),
    path('logout/',views.LogoutUserView.as_view(),name='logout'),
    path('',views.DashbordUserView.as_view(),name='dashboard'),
    path('myblog/',views.MyblogUserView.as_view(),name='myblog'),
    path('create/post/',views.CreatePostView.as_view(),name='create-post'),
    path('users/',views.UsersListView.as_view(),name='users'),
    path('users/delete/<int:id>',views.DeleteUserView.as_view(),name='delete-users'),
]
