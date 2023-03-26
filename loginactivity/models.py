from django.db import models
from accounts.models import User
from core.utils.models import UUIDInjector
# Create your models here.
class LoginActivity(UUIDInjector):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True)
    success = models.BooleanField(default=False)
    password_error = models.BooleanField(default=False)
    email_error = models.BooleanField(default=False)
    email = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.email