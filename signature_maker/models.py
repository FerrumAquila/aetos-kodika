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


class Signature(TrackingFields):
    html = models.TextField(max_length=1000)
    components = ArrayField(models.CharField(max_length=20, blank=True, null=True), size=10, blank=True, null=True)

    def save(self, *args, **kwargs):
        components_list = [part.split(")s")[0] for part in self.html.split("%(")][1:]
        self.components = components_list
        super(Signature, self).save(*args, **kwargs)
