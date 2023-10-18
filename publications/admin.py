from django.contrib import admin
from .models import Category, Reaction, Publication, Comment

# Register your models here.

admin.site.register(Category)
admin.site.register(Reaction)
admin.site.register(Publication)
admin.site.register(Comment)
