import uuid
from django.db import models
from django.conf import settings


STATUSES = (
    ('Approved', 'Approved'),
    ('Completed', 'Completed'),
    ('Rejected', 'Rejected'),
    ('Not started', 'Not started'),
    ('In progress', 'In progress'),
)

User = settings.AUTH_USER_MODEL



class DateRange(models.Model):
    start_on = models.DateField()
    end_on = models.DateField()

    class Meta:
        abstract = True


class DateTimeRange(models.Model):
    start_on = models.DateTimeField()
    end_on = models.DateTimeField()

    class Meta:
        abstract = True


class UUIDInjector(models.Model):
    _id = models.CharField(default=uuid.uuid1, max_length=250, unique=True)

    class Meta:
        abstract = True


class TimeStamp(models.Model):
    """ Add created and modified date, owner and modifier to each object created
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        abstract = True

class TimeStampNoUser(models.Model):
    """ Add created and modified date, owner and modifier to each object created
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class NameFieldInjector(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True


class GPSFieldInjector(models.Model):
    lng = models.FloatField(default=0.00, null=True, blank=True)
    lat = models.FloatField(default=0.00, null=True, blank=True)

    class Meta:
        abstract = True


class ApprovalFieldsInjector(models.Model):
    """ Add created and modified date, owner and modifier to each object created
    """
    status = models.CharField(max_length=50, default='Not started',  choices=STATUSES, null=True, blank=True)
    rejected_at = models.DateTimeField(blank=True, null=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

