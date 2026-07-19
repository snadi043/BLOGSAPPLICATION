from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# This is the file which is responsible to make the communication work in between the database and the application.
# Django by itself provide a default database file i,e db.sqlite3 for every project where, the details about the 
# databases that are needed in the application has to be configured.
# If the requirement is to proceed with a NON SQL database, then the neccessary modules and packages has to be installed.
# Here, in the SQL since it is a Structured Query Language, the data is represented within Tables as Rows and Columns.
# So, the models in Django are designed in a way that, the schema for the fileds of the database has to be declared so that
# next steps in the proccess will be handled by Django.

# In Django models which are basically classes similar to the python classes Django Models also has built in methods,
# which can translate the data of the models and the changes to these methods can be done accordingly.

class Tag(models.Model):
    caption = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.caption

class Author(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    email = models.EmailField(null=False, unique=True)

    class Meta:
        indexes = [
            models.Index(fields=["last_name", "first_name"])
        ]

        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def get_author_fullName(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.get_author_fullName()
    
# This is the model class for the ReviewForm which is the ORM needed to store the values from the form to the database. 

class Blog(models.Model):
    title = models.CharField(max_length=100, null=False, unique=True)
    # One author many posts, the idea here is to create a OneToMany relation between Authors and Blogs.
    author = models.ForeignKey(
            to=Author,
            related_name="blogs",
            on_delete=models.CASCADE, 
            null=False
            )
    imageUrl = models.ImageField(upload_to="myblogs/images", null=True)
    # imageUrl = models.ImageField(upload_to='myblogs/images', blank="True", null="True")
    updatedOn = models.DateTimeField(auto_now=True, null=False)
    excerpt = models.CharField(max_length=250, null=False)
    summary = models.CharField(max_length=2000, null=False)
    slug = models.SlugField(unique=True, null=False)
    tags = models.ManyToManyField(to=Tag, related_name="blogTags")

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

class ReviewsModel(models.Model):
    reviewer_name = models.CharField(null=True, max_length=20)
    reviewer_email = models.EmailField()
    reviewer_review = models.TextField(null=True, max_length=400)
    reviewer_rating = models.IntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    blog = models.ForeignKey(to=Blog, on_delete=models.CASCADE, related_name="reviews")


class UserProfileImage(models.Model):
    userImage = models.FileField(upload_to="myblogs/images/uploads", null=True)
    
# class CommentsModel(models.Model):
#     username = models.CharField(null=True, unique=True)
#     email = models.EmailField()
#     comment = models.TextField(null=True, max_length = 400)
#     blog = models.ForeignKey(to=Blog, on_delete=models.CASCADE, related_name="comments")
