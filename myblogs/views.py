from django.shortcuts import render, get_object_or_404

from django.http import Http404, HttpResponseRedirect

from .models import Blog, UserProfileImage

from .forms import ReviewForm, CreateUserProfileForm

from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormView




def store_file(file):
    with open('temp/images', 'wb+') as dest:
        for chunk in file.chunks:
            dest.write(chunk)

from django.views.generic.edit import FormView

from django.views.generic.edit import FormView

# Create your views here.

# Creating the class based View by importing the View library from the django.views
# class ReviewView(View):
#     # in the class based view the functions are handled by built in HTTP methods.
#     # get() method to handle the GET request response for the Review view.
#     def get(self, request):
#         form = ReviewForm()
#         return render(request, "myblogs/review.html", {"form": form})
    
#     # post() method to handle the POST request response for the Review view.
#     def post(self, request):
#         form = ReviewForm(request.POST)

#         if form.is_valid:
#             form.save()
#             return HttpResponseRedirect('posts/thank-you')
        
#         return render(request, "myblogs/review.html", {"form": form})


# Creating the class based FormView by importing the FormView library from the django.views.generic.edit
class ReviewView(FormView):
    form_class = ReviewForm
    template_name = 'myblogs/review.html'
    success_url = 'posts/thankyou'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

class UserProfileList(ListView):
    model = UserProfileImage
    template_name = 'myblogs/user-profile-list.html'
    success_url = 'posts/userprofilelist'
    
# class UserProfileView(View):
#     def get(self, request):
#         form = UserProfileForm()
#         return render('myblogs/create-profile.html', {"form": form})
    
#     def post(self, request):
#         submitted_form = UserProfileForm(request.POST, request.FILES)

#         if submitted_form.is_valid():
#             store_file(request.FILES['image'])
#             return HttpResponseRedirect('/myblogs/thank-you')
#         else:
#             return render(request, "myblogs/create-profile.html", {"form" : submitted_form})


# Creating the class based View for the purpose of creating the user profile by importing the View library from the django.views
class CreateUserProfileView(View):
    def get(self, request):
        form = ReviewForm()
        return render(request, "myblogs/review.html", {"form": form})
    
    def post(self, request):
        submitted_form = CreateUserProfileForm(request.POST, request.FILES)

        if submitted_form.is_valid():
            # store_file(request.FILES['image'])
            user_profile_image = UserProfileImage(userImage=request.FILES['image'])
            user_profile_image.save()
            return HttpResponseRedirect('/posts/thankyou')
        else:
            return render(request, "myblogs/create-profile.html", {"form" : submitted_form})

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

# # This is the response / view which has to be rendered when all the posts of the application is triggered.
# def posts(request):
#     all_posts = Blog.objects.all().order_by('-updatedOn') 

#     return render(request,'myblogs/all-posts.html', 
#         {
#             "posts": all_posts[:]
#         }
#     )

# This is the class based view for all-posts which has to be rendered when all the posts of the application is triggered.
class PostsView(TemplateView):
    template_name = "myblogs/all-posts.html"
    model = Blog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_posts = Blog.objects.all().order_by('-updatedOn')
        
        context["all_posts"] = loaded_posts
        context["posts"] = list(loaded_posts)
        
        return context
    
    # def get(self,request, *args, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["session_value"] = self.request.session.get('favorite_id')
    #     context["all_posts"] = Blog.objects.all().order_by('-updatedOn')[:]
        
    #     return context
        
            

# This is the response / views which has to be rendered when an individual post from the list of posts of the application is triggered.
class PostDetailView(DetailView):
    template_name = 'myblogs/post-detail.html'
    model = Blog
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = self.object.tags.all()
        return context
    

# def post_detail(request, slug):
#     posts = get_object_or_404(Blog, slug=slug)
#     print(posts, 'PostDetail')

#     return render(request,'myblogs/post-detail.html', 
#         {
#             "posts": posts,
#             "tags": posts.tags.all(),
#         }
#     )

# This is the response / views which has to be rendered when a user want to write a review on the post from the posts details page of the application.
# def review(request):
#     # On the request object in django, it is possible to access what type of HTTP request are triggered and extract the required data from it.
#     # In the POST method, it is a regular practice to extract the form input data to then store it in the database/local storage depending on the requirement.
#         # entered_username = request.POST['username']
#         # entered_reviewData = request.POST['review-data']
#         # print(entered_username, entered_reviewData)

#     if request.method == "POST":
#         existing_data = get_object_or_404(ReviewModel, id="pk")
#         # Instantiating the ReviewForm class to then pass the POST method information to check if the form is valid or not.
#         form = ReviewForm(request.POST, instance=existing_data)
#         if form.is_valid:
#             # Instantiating the reviewForm from the models file to feed it with the data retrieved from the form through cleaned_data object
#             # and saving it to the database which is handled by the models class by Django behind the scenes, once the migrations are successfull.
#             # reviewModel = ReviewModel(
#             #     username = form.cleaned_data['username'],
#             #     reviewData = form.cleaned_data['reviewData'],
#             #     rating = form.cleaned_data['rating'],
#             # )
#             # This process of initializing the model import and saving it doesnot work since there is not built-in save() method on the Model unless 
#             # the model is a FormModel in the Forms in the Django Framework.
#             form.save()
#         # In general the best practise to handle the POST request after the data is retrived is to redirect it to the dedicated page by using Django built in HTTP
#         # methods which is HttpResponseRedirect()
#             return HttpResponseRedirect('posts/thank-you')
    
#     # If the method is not a POST method, then this will render the empty ReviewForm.
#     else:
#         form = ReviewModel(instance = existing_data)
#     return render(request, "myblogs/review.html", 
#             {
#                 "form": form
#             })

# This is the response / views which has to be rendered to a user after thr review for the post is written.
# def thankyou(request):
#     return render(request, 'myblogs/thankyou.html')

# This is the class based view for the thankyou page after the user writes a review on the blog in the application.
class ThankyouView(View):
    
    def get(self, request):
        return render(request, 'myblogs/thankyou.html')

    def post(self, request):
        return render(request, 'myblogs/thankyou.html')

# This is the response / views which has to be rendered when an error in the application is triggered.
def ErrorPage(request):
    raise Http404()


