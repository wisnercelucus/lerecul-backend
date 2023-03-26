from django.contrib import admin
from .models import LoginActivity

class LoginActivityAdmin(admin.ModelAdmin):
    pass

# Register your models here.
admin.site.register(LoginActivity, LoginActivityAdmin)