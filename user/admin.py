from django.contrib import admin
from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'last_login', 'phone_number']
    ordering = ['last_login']
    search_fields = ['email', 'username', 'phone_number']