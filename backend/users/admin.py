from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import Follow, UserProfile


@admin.register(UserProfile)
class UserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')


@admin.register(Follow)
class FollowAdmin(UserAdmin):
    list_display = ('id', 'user', 'following')
    search_fields = ('user', 'following')
    list_filter = ('user', 'following')
