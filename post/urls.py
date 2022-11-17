from django.urls import path
from . import views

app_name = "post"

urlpatterns = [
    path("", views.index, name="home"),
    path("search/", views.search, name="search"),
    path("<int:id>/", views.detail, name="detail"),
    path("delete/<int:id>/", views.DeletePost, name="delete"),
    path("update/<int:id>/", views.UpdatePost, name="update"),
]
