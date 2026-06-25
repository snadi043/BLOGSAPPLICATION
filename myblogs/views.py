from django.shortcuts import render

from django.http import HttpResponse, Http404

# Create your views here.
# This is the response / view which has to be rendered when the landing page of the application is triggered.
def index(request):
    return render(request,'myblogs/index.html', 
        {
            "pageTitle": "Home"
        }
    )

# This is the response / view which has to be rendered when all the posts of the application is triggered.
def posts(request):
    return render(request,'myblogs/all-posts.html', 
        {
            "pageTitle": 'All Posts'
        }
    )

# This is the response / views which has to be rendered when an individual post from the list of posts of the application is triggered.
def post_detail(request, slug):
    return render(request,'myblogs/post-detail.html', 
        {
            "pageTitle": slug,
            "postTitle": slug
        }
    )

# This is the response / views which has to be rendered when an error in the application is triggered.
def ErrorPage(request):
    raise Http404()
