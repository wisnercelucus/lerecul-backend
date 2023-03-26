from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, UserProfile, UserRole, UserPosition


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active', 'is_admin', 'is_superuser',)
    list_filter = ('email', 'is_staff', 'is_active', 'is_admin', 'groups', 'is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'name', 'username', 'password'),}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'is_admin', 'groups', 'user_permissions', 'roles', 'frontend_views',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active','is_admin', 'is_superuser',)}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions', 'roles',)

class UserProfileAdmin(admin.ModelAdmin):
    pass


class UserRoleAdmin(admin.ModelAdmin):
    pass


class UserPositionAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(UserPosition, UserPositionAdmin)
