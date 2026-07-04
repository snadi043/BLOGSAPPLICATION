from django import forms

class ReviewForm(forms.Form):
    username = forms.CharField(
        label="Your Name",
        min_length=5,
        max_length=15, 
        required=True, 
        error_messages={"required": "Your name should be atleast 5 to 15 charecters long."})
    
    reviewData = forms.CharField(
        label="Your Review", 
        min_length=25,
        max_length=100,
        required=True,
        error_messages={"required": "Your review should be atleast 25 to 100 charecters long."}
        )

