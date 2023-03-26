from django.contrib import admin
from .models import FrontEndMenuLink


class FrontEndMenuLinkAdmin(admin.ModelAdmin):
    pass

admin.site.register(FrontEndMenuLink, FrontEndMenuLinkAdmin)
