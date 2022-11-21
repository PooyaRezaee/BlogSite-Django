from django.urls import path
from . import views

app_name = "post"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("<int:id>/", views.DetailView.as_view(), name="detail"),
    path("delete/<int:id>/", views.DeletePostView.as_view(), name="delete"),
    path("update/<int:id>/", views.UpdatePostView.as_view(), name="update"),
    path("author/", views.AuthorListView.as_view(), name="authors"),
    path("author/<int:id>/", views.AuthorPostListView.as_view(), name="author"),
]
