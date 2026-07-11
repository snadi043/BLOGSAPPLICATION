from django import forms

from .models import Review

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

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['username', 'reviewData', 'rating']