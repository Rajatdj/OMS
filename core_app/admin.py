from django.contrib import admin
from .models import UserDetails, Token

admin.site.register(UserDetails)
admin.site.register(Token)

