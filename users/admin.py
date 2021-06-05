from django.contrib import admin

from .models import User
from graphql_auth.models import UserStatus

admin.site.register(User)
admin.site.register(UserStatus)

