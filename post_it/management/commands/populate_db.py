from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

import random
from post_it.models import ProfileDetails, Tweet


class Command(BaseCommand):
    def populate_fake_profiles(self):
        ProfileDetails.objects.all().delete()
        for username in "ABCDEFGHIJ":
            new_user = User(email=str(str(username) + "@gmail.com"), username=str(username))
            new_user.save()
            new_user.set_password("vishesh23")
            new_user.save()
            profile = ProfileDetails(username=str(username), user=new_user, email=str(str(username) + "@gmail.com"),
                                     gender="F")
            profile.save()
            print "Fake Profile Username '" + str(profile.username) + "' Created!!!"

    def populate_fake_tweets(self):
        Tweet.objects.all().delete()
        for profile in ProfileDetails.objects.all():
            for t in "1234567":
                tweet = Tweet(author=profile, text=str(t))
                tweet.save()
                print "Fake Tweet '" + str(tweet.text) + "' by '" + str(profile.username) + "' Created!!!"

    def populate_fake_tag_tweets(self):
        for profile in ProfileDetails.objects.all():
            for t in "890":
                tweet = Tweet(author=profile, text=str(t))
                tweet.save()
                tweet.tags.add(ProfileDetails.objects.all()[random.randint(0, 9)])
                print "Fake Tweet '" + str(tweet.text) + "' by '" + str(profile.username) + "' with '" + str(
                    tweet.tags.get_queryset()[0].username) + "' Created!!!"

    def handle(self, *args, **options):
        self.populate_fake_profiles()
        self.populate_fake_tweets()
