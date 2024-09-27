from django.contrib import admin
from .models import CustomUser,Post,Like,Review
admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Review)



