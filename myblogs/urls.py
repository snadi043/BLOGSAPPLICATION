# This file is as similar as the urls.py file in the project level.
# It is mandatory to configure this file to handle the navigation within the application and respond with respective views for 
# every individual request made to the server.
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="landing-page"),
    path('posts', views.posts, name="all-posts"),
    path('posts/<str:postname>', views.post_detail, name="posts-details")
    # slug:slug
]
