from django.shortcuts import render, get_object_or_404

from django.http import Http404 

from .models import Blog

# Create your views here.

# This is the response / view which has to be rendered when the landing page of the application is triggered.
def index(request):
    # sorted_posts = sorted(dummy_posts, key=getDate)
    # latest_posts = sorted_posts[-2:]

    latest_posts = Blog.objects.all().order_by('-updatedOn')[:3]

    return render(request,'myblogs/index.html', 
        {
            "posts": latest_posts
        }
    )

# This is the response / view which has to be rendered when all the posts of the application is triggered.
def posts(request):
    all_posts = Blog.objects.all().order_by('-updatedOn') 

    return render(request,'myblogs/all-posts.html', 
        {
            "posts": all_posts[:]
        }
    )

# This is the response / views which has to be rendered when an individual post from the list of posts of the application is triggered.
def post_detail(request, slug):
    posts = get_object_or_404(Blog, slug=slug)
    return render(request,'myblogs/post-detail.html', 
        {
            "posts": posts,
            "tags": posts.tags.all()
        }
    )

# This is the response / views which has to be rendered when an error in the application is triggered.
def ErrorPage(request):
    raise Http404()
