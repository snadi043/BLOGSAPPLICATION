# This file is as similar as the urls.py file in the project level.
# It is mandatory to configure this file to handle the navigation within the application and respond with respective views for 
# every individual request made to the server.
from django.urls import path

from . import views

urlpatterns = [
    path('', views.StartingPageView.as_view(), name="landing-page"),
    path('create-profile', views.CreateUserProfileView.as_view(), name="create-user-profile"),
    path('user-profile-list', views.UserProfileList.as_view(), name="user-profile-list"),
    path('posts', views.PostsView.as_view(), name="all-posts"),
    # slug:slug
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name="posts-details"),
    path('posts/review', views.ReviewView.as_view(), name="posts-review-form"),
    path('posts/thank-you', views.ThankyouView.as_view(), name="thank-you")
]
