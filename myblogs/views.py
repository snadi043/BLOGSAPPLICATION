from django.shortcuts import render, get_object_or_404

from django.http import Http404, HttpResponseRedirect

from .models import Blog

from .forms import ReviewForm

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

# This is the response / views which has to be rendered when a user want to write a review on the post from the posts details page of the application.
def review(request):
    # On the request object in django, it is possible to access what type of HTTP request are triggered and extract the required data from it.
    # In the POST method, it is a regular practice to extract the form input data to then store it in the database/local storage depending on the requirement.
        # entered_username = request.POST['username']
        # entered_reviewData = request.POST['review-data']
        # print(entered_username, entered_reviewData)

    if request.method == "POST":
        # Instantiating the ReviewForm class to then pass the POST method information to check if the form is valid or not.
        form = ReviewForm(request.POST)
        if form.is_valid:
        # In general the best practise to handle the POST request after the data is retrived is to redirect it to the dedicated page by using Django built in HTTP
        # methods which is HttpResponseRedirect()
            return HttpResponseRedirect('posts/thank-you')
    
    # If the method is not a POST method, then this will render the empty ReviewForm.
    else:
        form = ReviewForm()
    return render(request, "myblogs/review.html", 
            {
                "form": form
            })

# This is the response / views which has to be rendered to a user after thr review for the post is written.
def thankyou(request):
    return render(request, 'myblogs/thankyou.html')

# This is the response / views which has to be rendered when an error in the application is triggered.
def ErrorPage(request):
    raise Http404()
