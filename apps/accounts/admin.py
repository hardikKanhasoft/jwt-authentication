from django.contrib import admin
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "name", "is_tc", "is_admin"]
    ordering = ["id"]
admin.site.register(User, UserAdmin)
