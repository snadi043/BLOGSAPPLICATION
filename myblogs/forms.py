from django import forms

from .models import ReviewModelForm

# class ReviewForm(forms.Form):
#     username = forms.CharField(
#         label="Your Name",
#         min_length=5,
#         max_length=15, 
#         required=True, 
#         error_messages={"required": "Your name should be atleast 5 to 15 charecters long."})
    
#     reviewData = forms.CharField(
#         label="Your Review",
#         widget=forms.Textarea(attrs={"rows":"20", "cols":"47"}),
#         min_length=25,
#         max_length=250,
#         required=True,
#         error_messages={"required": "Your review should be atleast 25 to 100 charecters long."})
    
#     rating = forms.IntegerField(
#         label="Your Rating",
#         required=True,
#         min_value= 1,
#         max_value=5,
#         error_messages={"required": "Please enter a rating within 1 to 5."})

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

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewModelForm
        fields = ['username', 'email', 'reviewData', 'rating']
        labels = {
            "username": "Your Name",
            "email": "Your Email",
            "reviewData": "Your Review",
            "rating": "Your Rating"
        }
        