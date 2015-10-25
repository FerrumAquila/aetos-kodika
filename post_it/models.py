from django.db import models
from django.contrib.auth.models import User

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


class ProfileDetails(TrackingFields):
    user = models.ForeignKey(User, related_name='profile')
    username = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=2)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    data = models.TextField(blank=True)
    following = models.ManyToManyField('self', related_name='followers')

    def __unicode__(self):
        return self.username + "'s Profile"

    def get_follow_suggestion(self):
        exclude_ids = self.following.all().values_list('id', flat=True) + [self.id]
        return ProfileDetails.objects.all().exclude(id__in=exclude_ids).order_by("-id")


class Sticky(TrackingFields):
    author = models.ForeignKey(ProfileDetails, related_name='stickies')
    text = models.TextField(max_length=1000)
    tags = models.ManyToManyField(ProfileDetails, related_name='tagged_in')


class StickyOnSticky(TrackingFields):
    top_sticky = models.ForeignKey(Sticky, related_name='posted_for')
    reply_sticky = models.ForeignKey(Sticky, related_name='posted_on')

    @classmethod
    def post_sticky(cls, top_sticky, reply_sticky):
        instance = cls(top_sticky=top_sticky, reply_sticky=reply_sticky)
        instance.save()
        instance.reply_sticky.tags.add(ProfileDetails.objects.get(username=str(instance.top_sticky.author.username)))