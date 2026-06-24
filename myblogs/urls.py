from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="landing-page"),
    path('posts', views.posts, name="all-posts"),
    path('posts/<str:postname>', views.post_detail, name="posts-details")
    # slug:slug
]
