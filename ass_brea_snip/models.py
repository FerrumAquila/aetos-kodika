from django.contrib.postgres.fields import ArrayField
from django.db import models

# from IPython.frontend.terminal.embed import InteractiveShellEmbed
# InteractiveShellEmbed()()


class TrackingFields(models.Model):
    """
    Each model will have these fields
    """
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

