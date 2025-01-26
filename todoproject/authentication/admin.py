from django.contrib import admin
from .models import CustomUser

# Register your models here.

admin.site.register(CustomUser)
admin.site.site_header = 'Fresh Start Administrator'  # Login page title
admin.site.site_title = 'Fresh Start Admin'  # Browser tab title
admin.site.index_title = 'Welcome to Fresh Start Management'  # Admin index page titlemy