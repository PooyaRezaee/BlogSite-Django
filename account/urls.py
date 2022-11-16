from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.regiser,name='register'),
    path('login/',views.LoginUser,name='login'),
    path('logout/',views.LogoutUser,name='logout'),
]
