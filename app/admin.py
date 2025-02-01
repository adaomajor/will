from django.contrib import admin
from app.models import user, post, like

# Register your models here.

admin.site.register(user)
admin.site.register(post)
admin.site.register(like)