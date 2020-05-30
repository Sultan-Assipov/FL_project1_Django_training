from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "teacher", "student", "group")
    pass


admin.site.register(User, UserAdmin)