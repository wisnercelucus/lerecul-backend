from django.db import models

# Create your models here.
class NewsSubscriber(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    email = models.EmailField(max_length=70, unique=True)

    def __str__(self):
        return self.email


class ContactMessage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=70)
    phone = models.CharField(max_length=70, blank=True, null=True)
    subject = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField()
    country = models.CharField(max_length=50, null=True, blank=True)
    country_code = models.CharField(max_length=10, null=True, blank=True)
    emailed_success = models.BooleanField(default=False)

    def __str__(self):
        return self.email


