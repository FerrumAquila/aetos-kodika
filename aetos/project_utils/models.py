__author__ = 'ironeagle'

from django.db import models


class TrackingFields(models.Model):
    """
    Each model will have these fields
    """
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
