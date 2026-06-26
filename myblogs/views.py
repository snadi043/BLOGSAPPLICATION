from django.shortcuts import render

from django.http import HttpResponse, Http404

from datetime import datetime

# Create your views here.

# Creating a dummy dictionary to make the dynamic representation of data in the DTL templates.
dummy_posts = [
    {
        # When declaring the values for the "slug" always make sure that there are no spaces in the value of the slug because 
        # Django cannot understand the void spaces in between the names and throws unidentified error.
        "slug": "my-mind",
        "title": "How to really write a 'blog'.",
        "updatedOn": datetime.now(),
        "author": "SAI SOUL",
        "imageName": "blog-icon.png",
        "excerpt": "Blog Your Though, is a platform where you can create memories of your thoughts which can be random, creative...",
        "summary": """There is lot of change in my perspective whenever I give a thought about life since last 3 years.
                    It is completely a mixed reaction with lot of emotions for which I am happy in a way but again when involved 
                    with little bit of serious disscussions about life within family or friends I am like "What am I doing here?" """
    },
    {
        "slug": "my-heart",
        "title": "Joyful blog about limiting yourself",
        "updatedOn": datetime(1995, 12, 19),
        "author": "SAI HEART",
        "imageName": "blog-icon.png",
        "excerpt": "Blog Your Though, is a platform where you can create memories of your thoughts which can be random, creative...",
        "summary": """Lorem ipsum dolor sit amet consectetur adipisicing elit. Explicabo, dolor laborum similique tempore harum iusto nisi ipsa error ullam perspiciatis nihil vitae ex inventore, 
                    cum facere! Nemo fugit suscipit ducimus.
                    Lorem ipsum dolor sit amet consectetur adipisicing elit. Explicabo, dolor laborum similique tempore harum 
                    """
    },
    {
        "slug": "my-right",
        "title": "Voice about Vurtue",
        "updatedOn": datetime(2013, 2, 9),
        "author": "SAI HEART",
        "imageName": "blog-icon.png",
        "excerpt": "This one is about my personality which I got to develop by understanding the surroundings, situations and  sacrifies...",
        "summary": """Often times, in this life you are pushed to be in situations where you have to call for decisions which might not show any impact
                    on your job, salary or your benefits in life but later down the lane when you get the sudden thought about that decisive decission you once
                    made from the past can stop you for a while and make you regretful."""
    }
]

def getDate(post):
    return post['updatedOn']

# This is the response / view which has to be rendered when the landing page of the application is triggered.
def index(request):
    sorted_posts = sorted(dummy_posts, key=getDate)
    latest_posts = sorted_posts[-2:]

    return render(request,'myblogs/index.html', 
        {
            "posts": latest_posts
        }
    )

# This is the response / view which has to be rendered when all the posts of the application is triggered.
def posts(request):
    return render(request,'myblogs/all-posts.html', 
        {
            "posts": dummy_posts[:]
        }
    )

# This is the response / views which has to be rendered when an individual post from the list of posts of the application is triggered.
def post_detail(request, slug):
    identified_post = next(post for post in dummy_posts if post['slug'] == slug)
    return render(request,'myblogs/post-detail.html', 
        {
            "post": identified_post,
            
        }
    )

# This is the response / views which has to be rendered when an error in the application is triggered.
def ErrorPage(request):
    raise Http404()
