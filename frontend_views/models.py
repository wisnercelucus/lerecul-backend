from django.db import models

from core.utils.models import UUIDInjector


class FrontEndMenuLink(UUIDInjector):
    name = models.CharField(max_length=100)
    tab = models.CharField(max_length=20)
    codename = models.CharField(max_length=50)
    visibility_code = models.CharField(max_length=100, blank=True, null=True)
    has_link = models.BooleanField(default=True)
    root_link=models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return self.tab + '|' + self.codename + '|' + self.name 