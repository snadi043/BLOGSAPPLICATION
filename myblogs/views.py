from django.shortcuts import render

from django.http import HttpResponseRedirect

from django.urls import reverse

from .models import Blog, UserProfile, ReviewsModel

from .forms import CreateUserProfileForm, ReviewsForm

from django.views.generic import ListView, View, TemplateView


def store_file(file):
    with open('temp/images', 'wb+') as dest:
        for chunk in file.chunks:
            dest.write(chunk)

class UserProfileList(ListView):
    model = UserProfile
    template_name = 'myblogs/user-profile-list.html'
    success_url = '/posts/userprofilelist'
    context_object_name = 'profiles'
    profiles = UserProfile.objects.all()

    print(profiles, 'UserProfileList')
    

# Creating the class based View for the purpose of creating the user profile by importing the View library from the django.views
class CreateUserProfileView(View):
    def get(self, request):
        form = CreateUserProfileForm()
        profiles = UserProfile.objects.all()

        context = {
            "profiles": profiles,
            "form" : form
        }

        return render(request, "myblogs/create-profile.html", context)
    
    def post(self, request):
        submitted_form = CreateUserProfileForm(request.POST, request.FILES)

        if submitted_form.is_valid():
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            email = request.POST.get('email')
            userImage=request.FILES.get('image')

            user_profile_data = UserProfile(first_name = first_name, last_name = last_name, email = email, userImage = userImage)
            
            user_profile_data.save()
            
            context = {
                "profiles": user_profile_data,
                "submitted_form" : submitted_form
            }
        
            return HttpResponseRedirect('/posts/thankyou')
        else:
            return render(request, "myblogs/create-profile.html", context)

# This is the response / view which has to be rendered when the landing page of the application is triggered.
class StartingPageView(ListView):
    # In the CBV(class based views) template view is rendered by enabling the 
    # default class varibale "template_name" to the desired "HTML" file of your choice.
    # If you have data which has the CRUD operations to be (ORM) performed the model variable has to be set.
    # If the template has extended template and the context has to be available in all the HTML files then the variable "context_object_name" has to be set.
    template_name = "myblogs/index.html"
    model = Blog
    context_object_name = "posts"
    data = Blog.objects.all()
    ordering = data.order_by("-updatedOn")

    # Also in the CBV the database communications can be customized by refactoring the default function in the respective class extension formats.
    def get_queryset(self):
        data = Blog.objects.all()
        latest_posts = data[:3]
        return latest_posts


# This is the class based view for all-posts which has to be rendered when all the posts of the application is triggered.
class PostsView(ListView):
    template_name = "myblogs/all-posts.html"
    model = Blog
    ordering = ["-updatedOn"]
    context_object_name = "posts"
    

# This is the response / views which has to be rendered when an individual post from the list of posts of the application is triggered.
# General View extension cannot automatically identify the dynamic slug filed in the CBV but the DetailView can identify and route accordingly. 
class PostDetailView(View):
    def stored_blogs_session(self, request, blog_id):
        stored_blogs = request.session.get('read_later_posts')
        if stored_blogs is not None:
            is_saved_for_later = blog_id in stored_blogs
        else: 
            is_saved_for_later = False
        return is_saved_for_later
    

    def get(self, request, slug):
        blog = Blog.objects.get(slug=slug)
        review_data = blog.reviews.all().order_by('reviewer_rating')
        
        context = {
            "blog": blog,
            "tags": blog.tags.all(),
            "reviews": review_data,
            "saved_for_later": self.stored_blogs_session(request, blog.id)
        }
        return render(request, "myblogs/post-detail.html", context)
    
    def post(self, request, slug):
        blog = Blog.objects.get(slug=slug)        

        context = {
            "blog": blog,
            "tags": blog.tags.all(),
        }
        return render(request, "myblogs/post-detail.html", context)
    
# This is the class based view for read-later which has to be rendered 
# when user clicks on read-later button from the post-details page of the application is triggered.
class ReadLaterView(View):
    def get(self, request):
        stored_blogs = request.session.get('read_later_posts')

        context = {}

        if stored_blogs is None or len(stored_blogs) == 0:
            context['has_blogs'] = False
            context['blogs'] = stored_blogs
        
        else: 
            blog = Blog.objects.filter(id__in=stored_blogs)
            context['blogs'] = blog
            context['has_blogs'] = True

        return render(request, 'myblogs/read-later.html', context)

    def post(self, request):
        stored_blogs = request.session.get('read_later_posts')

        if stored_blogs is None:
            stored_blogs = []

        blog = int(request.POST.get('blog_id'))
        
        if blog not in stored_blogs:
            stored_blogs.append(blog)
        else:
            stored_blogs.remove(blog)

        request.session['read_later_posts'] = stored_blogs
            
        return HttpResponseRedirect('/')

# Creating the class based FormView by importing the FormView library from the django.views.generic.edit
class ReviewView(View):

    def get(self, request, slug):
        blog = Blog.objects.get(slug=slug)
        reviews = ReviewsModel.objects.all()

        context = {
            "blog": blog,
            "review_data": reviews,
            "review_form": ReviewsForm(),
        }
        return render(request, 'myblogs/review.html', context)

    def post(self, request, slug):
        review_form = ReviewsForm(request.POST)
        blog = Blog.objects.get(slug=slug)
        reviews = blog.reviews.all()

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.blog = blog
            review.save()
            return HttpResponseRedirect(reverse('posts-details', args=[slug]))
        
        context = {
            "blog": blog,
            "review_form": review_form,
            "review_data": reviews
        }
        return render(request, 'myblogs/review.html', context)
    

    
# This is the class based view for the thankyou page after the user writes a review on the blog in the application.
class ThankyouView(TemplateView):
    
    def get(self, request):
        return render(request, 'myblogs/thankyou.html')

    def post(self, request):
        return render(request, 'myblogs/thankyou.html')

# This is the response / views which has to be rendered when an error in the application is triggered.
class ErrorPageView(TemplateView):
    template_name = "404.html"

    # Over writing the render_to_response() to set the status key and comparing it with 404 error code.
    def render_to_response(self, context, **response_kwargs):
        response_kwargs['status'] = 404
        return super().render_to_response(context, **response_kwargs)


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




# def index(request):
#     # sorted_posts = sorted(dummy_posts, key=getDate)
#     # latest_posts = sorted_posts[-2:]

#     latest_posts = Blog.objects.all().order_by('-updatedOn')[:3]

#     return render(request,'myblogs/index.html', 
#         {
#             "posts": latest_posts
#         }
#     )

# # This is the response / view which has to be rendered when all the posts of the application is triggered.
# def posts(request):
#     all_posts = Blog.objects.all().order_by('-updatedOn') 

#     return render(request,'myblogs/all-posts.html', 
#         {
#             "posts": all_posts[:]
#         }
#     )


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
