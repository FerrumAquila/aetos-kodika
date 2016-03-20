# coding=utf-8
from django.contrib.auth.decorators import user_passes_test

__author__ = 'ironeagle'

import math

from . import models as app_models
from collections import Counter


# TODO: make general matrix class and use that as parent for SectorMap
class SectorMap(object):
    """
    import ass_brea_snip.utils as abs_utils
    data = [[0,1,0], [1,0,0], [0,0,1]]
    sector_map = abs_utils.SectorMap(data)
    old_map = sector_map.get_map_json()
    new_sector_map = abs_utils.SectorMap(old_map)
    if new_sector_map.get_map_json() == old_map:
        print 'great success!!!'
    else:
        print 'great success!!!......not'

    grid_map_1 = {
        '0__0': 2,
        '0__1': 1,
        '0__2': 2,
        '1__0': 1,
        '1__1': 2,
        '1__2': 2,
        '2__0': 2,
        '2__1': 2,
        '2__2': 1
    }

    grid_map_2 = {
        '0__0': 1,
        '0__1': 2,
        '0__2': 1,
        '1__0': 2,
        '1__1': 1,
        '1__2': 1,
        '2__0': 1,
        '2__1': 1,
        '2__2': 2
    }
    """

    def __init__(self, data=None):
        if data and type(data) == list:
            order = len(data)
            for y in data:
                if not len(y) == order:
                    raise ValueError('Uneven Matrix')
            self.data = data
            self.order = order
        if data and type(data) == dict:
            order = math.sqrt(len(data.keys()))
            if not order.is_integer():
                raise ValueError('Uneven Matrix')
            order = int(order)
            arr_data = [['' for j in range(0, order)] for i in range(0, order)]
            for key, value in data.items():
                x, y = key.split('__')
                arr_data[int(x)][int(y)] = value
            self.data = arr_data
            self.order = order

    def check_co_ordinates(self, x, y):
        if x > self.order or y > self.order:
            raise ValueError('Invalid co ordinates')

    def get_value(self, x, y):
        self.check_co_ordinates(x, y)
        return self.data[x][y]

    def set_value(self, x, y, value):
        self.check_co_ordinates(x, y)
        self.data[x][y] = value

    @property
    def get_map_json(self):
        return {'%s__%s' % (x, y): self.data[x][y] for x, row in enumerate(self.data) for y, r in enumerate(row)}


def abs_profile_required(view_func):
    def test_func(user):
        try:
            user.abs_profile
        except app_models.UserProfile.DoesNotExist:
            return False
        else:
            return True
    return user_passes_test(test_func=test_func)(view_func)


def get_or_create_challenge(challenger, challengee, match_id):
    return app_models.Challenge.objects.get_or_create(
        challenger=challenger, challengee=challengee, match=match_id
    )


def accept_challenge(challenge_id):
    challenge = app_models.Challenge.objects.get(id=challenge_id)
    challenge.state = app_models.Challenge.ACCEPTED
    challenge.save(update_fields=['state'])
    return challenge


def decline_challenge(challenge_id):
    challenge = app_models.Challenge.objects.get(id=challenge_id)
    challenge.state = app_models.Challenge.DECLINED
    challenge.save(update_fields=['state'])
    return challenge


def make_war(hitmen_tag, blackbrair_tag, hitmen_map, blackbrair_map):
    hitmen_strategy = make_strategy(hitmen_tag, hitmen_map)
    blackbrair_strategy = make_strategy(blackbrair_tag, blackbrair_map)
    war_stats = skirmish_results(hitmen_strategy, blackbrair_strategy)
    winner = determine_winner(war_stats)
    return winner


def make_strategy(gamer_tag, strategy_map):
    gamer = app_models.UserProfile.objects.get(gamer_tag=gamer_tag)
    strategy = app_models.Strategy(player=gamer, grid=strategy_map)
    strategy.save()
    return strategy


def skirmish_results(hitmen_strategy, blackbrair_strategy):
    survivor = lambda hitmen, blackbrair: hitmen_strategy.player if blackbrair in hitmen.can_kill.all()\
        else blackbrair_strategy.player
    soldier = lambda pk: app_models.Soldier.objects.get(pk=pk)
    shootout = [
        survivor(soldier(hitmen), soldier(blackbrair)) for (hitmen_pos, hitmen), (blackbrair_pos, blackbrair) in zip(
            hitmen_strategy.grid.items(), blackbrair_strategy.grid.items())
    ]
    return Counter(shootout)


def determine_winner(war_stats):
    return max(war_stats.iterkeys(), key=lambda k: war_stats[k])
