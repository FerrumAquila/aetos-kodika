# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres import fields as postgres_fields
from django.utils.functional import cached_property


class SoldierManager(models.Manager):
    def id_icon_map(self):
        return {i: {'pk': soldier.id, 'icon_class': soldier.bio['icon_class'], 'loadout': soldier.loadout}
                for i, soldier in enumerate(Soldier.objects.all().order_by('id'))}


class Soldier(models.Model):
    """
    Basic soldier model which stores the name and relates inferiors
    """
    loadout = models.CharField(max_length=60)
    can_kill = models.ManyToManyField('Soldier', related_name="killed_by")
    bio = postgres_fields.JSONField()
    objects = SoldierManager()

    def __unicode__(self):
        return self.loadout


class UserProfile(models.Model):
    gamer_tag = models.CharField(max_length=255)
    user = models.OneToOneField(User, related_name="abs_profile")

    def __unicode__(self):
        return self.gamer_tag


class SoldierLevel(models.Model):
    """
    Model that stores each player's soldier level
    """
    soldier = models.ForeignKey(Soldier, related_name="levels")
    user_profile = models.ForeignKey(UserProfile, related_name="soldiers")
    level = models.PositiveSmallIntegerField()

    class Meta(object):
        unique_together = ('soldier', 'user_profile')

    def __unicode__(self):
        return '|'.join((self.user_profile.gamer_tag, self.soldier.loadout, str(self.level)))


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
            self.salt = {str(sl.soldier.id): str(sl.level) for sl in self.player.soldiers.all()}
        super(Strategy, self).save(*args, **kwargs)


class Match(models.Model):
    """
    If you need docstring for this model, better kill yourself
    """
    hitmen = models.ForeignKey(Strategy, related_name="hitmen_matches", null=True)
    blackbriar = models.ForeignKey(Strategy, related_name="blackbriar_matches", null=True)

    @cached_property
    def result(self):
        from . import utils as abs_utils
        match_stats = abs_utils.skirmish_result(self.hitmen, self.blackbriar)
        return {'stats': match_stats, 'winner': abs_utils.determine_winner(match_stats)}


class Challenge(models.Model):
    """
    """
    ACCEPTED = 'accepted'
    DECLINED = 'declined'
    PENDING = 'pending'
    COMPLETED = 'completed'
    STATE_CHOICES = (
        (ACCEPTED, 'Accepted'),
        (DECLINED, 'Declined'),
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
    )
    challenger = models.ForeignKey(UserProfile, related_name="challenges")
    challengee = models.ForeignKey(UserProfile, related_name="challenged")
    match = models.ForeignKey(Match)
    state = models.CharField(max_length=20, default=PENDING,
                             choices=STATE_CHOICES)

    def __unicode__(self):
        return '{} \m/ {} | {}'.format(
            self.challenger, self.challengee, self.state
        )
