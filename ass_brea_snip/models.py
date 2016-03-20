# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres import fields as postgres_fields
from django.utils.functional import cached_property


class Soldier(models.Model):
    """
    Basic soldier model which stores the name and relates inferiors
    """
    loadout = models.CharField(max_length=60)
    can_kill = models.ManyToManyField('self', related_name="killed_by")


class UserProfile(models.Model):
    gamer_tag = models.CharField(max_length=255)
    user = models.OneToOneField(User, related_name="abs_profile")


class SoldierLevel(models.Model):
    """
    Model that stores each player's soldier level
    """
    soldier = models.ForeignKey(Soldier, related_name="levels")
    user_profile = models.ForeignKey(UserProfile, related_name="soldiers")
    level = models.PositiveSmallIntegerField()

    class Meta(object):
        unique_together = ('soldier', 'user_profile')


class Strategy(models.Model):
    """
    Stores the sector arrangement by a player
    and the snapshot of his/her soldier levels
    """
    grid = postgres_fields.JSONField()
    player = models.ForeignKey(UserProfile)
    salt = postgres_fields.HStoreField()
    created_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        first = not bool(self.pk)
        if first:
            self.salt = {sl.soldier.id: sl.level for sl in self.player.soldiers}
        super(Strategy, self).save(*args, **kwargs)


class Match(models.Model):
    """
    If you need docstring for this model, better kill yourself
    """
    hitmen = models.ForeignKey(Strategy, related_name="hitmen_matches")
    blackbriar = models.ForeignKey(Strategy, related_name="blackbriar_matches")

    @cached_property
    def winner(self):
        pass
