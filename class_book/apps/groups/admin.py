from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class MyUserAdmin(UserAdmin):
    list_display = ("username", "email", "teacher", "student", "group")
    fieldsets = UserAdmin.fieldsets + (
        ('School Status', {'fields': ('teacher',"student","group")}),
    )
    add_fieldsets = UserAdmin.fieldsets + (
        ('School Status', {'fields': ('teacher',"student","group")}),
    )


admin.site.register(User, MyUserAdmin)
