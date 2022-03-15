from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('username',
                    'first_name',
                    'last_name',
                    'email',
                    'role',
                    'bio')
    search_fields = ('username',
                     'first_name',
                     'last_name',
                     'email')
    list_filter = ('role',)
    empty_value_display = '-пусто-'


admin.site.register(User, CustomUserAdmin)
