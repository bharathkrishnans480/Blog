from django.contrib import admin
from blogapp.models import Blogs,Comments,UserProfile

admin.site.register(Blogs)
admin.site.register(Comments)
admin.site.register(UserProfile)