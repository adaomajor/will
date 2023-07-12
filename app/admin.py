from django.contrib import admin
from app.models import users, posts, likes

# Register your models here.

admin.site.register(users)
admin.site.register(posts)
admin.site.register(likes)