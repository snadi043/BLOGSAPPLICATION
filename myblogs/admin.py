from django.contrib import admin

# Register your models here.

from .models import Author,Blog,Tag,ReviewsModel

class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "slug", "updatedOn"]
    list_filter = ["author", "updatedOn", "tags"]
    prepopulated_fields = {"slug": ("title",)}

class AuthorAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email"]


class TagAdmin(admin.ModelAdmin):
    list_display = ["caption"]

class ReviewAdmin(admin.ModelAdmin):
    list_display = ["reviewer_name", "reviewer_rating", "blog"]


admin.site.register(Author, AuthorAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ReviewsModel, ReviewAdmin)
