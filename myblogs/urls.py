# This file is as similar as the urls.py file in the project level.
# It is mandatory to configure this file to handle the navigation within the application and respond with respective views for 
# every individual request made to the server.
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="landing-page"),
    path('posts', views.posts, name="all-posts"),
    # slug:slug
    path('posts/<slug:slug>/', views.post_detail, name="posts-details"),
    path('posts/review', views.review, name="posts-review-form"),
    path('posts/thank-you', views.thankyou, name="thank-you")
]
