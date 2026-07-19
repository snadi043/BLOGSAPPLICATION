from django import forms

from .models import ReviewsModel

class CreateUserProfileForm(forms.Form):
    firstname = forms.CharField(
        label="First Name",
        required=True,
        max_length=20,
        min_length=10,
        error_messages={"reqiured": "Please enter your firstname within 10-20 letters"})
    
    lastname = forms.CharField(
        label="Last Name",
        required=True,
        max_length=20,
        min_length=10,
        error_messages={"reqiured": "Please enter your lastname within 10-20 letters"})
    
    email = forms.EmailField(
        label="Email",
        required=True,
        error_messages={"reqiured": "Please enter a valid email address."})
    
    image = forms.FileField(
        label="Image",
        error_messages={"required": "Please browse and upload an image file."}
    )

class ReviewsForm(forms.ModelForm):
    class Meta:
        model = ReviewsModel
        fields = ['reviewer_name', 'reviewer_email', 'reviewer_review', 'reviewer_rating']
        labels = {
            "reviewer_name": "Your Name",
            "reviewer_email": "Your Email",
            "reviewer_review": "Your Review",
            "reviewer_rating": "Your Rating"
        }

# class CommentsForm(forms.ModelForm):
#     class Meta:
#         model = CommentsModel
#         fields = ['username', 'email', 'comment']
#         exclude = ["blog"]
#         labels = {
#             "username": "Your Name",
#             "email": "Your Email",
#             "comment": "Your Comment"
#         }
