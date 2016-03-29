# coding=utf-8
from django.contrib.auth.decorators import user_passes_test

__author__ = 'ironeagle'

import math

from . import models as app_models
from collections import Counter

json_match_result = lambda result: {'score': {key.gamer_tag: value for key, value in result['stats'].items()},
                                    'winner': result['winner'].gamer_tag}


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
        challenger=challenger, challengee=challengee, match_id=match_id
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


def fight_challenge(challenge_id, challengee_map):
    challenge = app_models.Challenge.objects.get(id=challenge_id, state=app_models.Challenge.ACCEPTED)
    challenge.state = app_models.Challenge.COMPLETED
    challenge_match = challenge.match
    challengee_strategy = make_strategy(challenge.challengee, challengee_map)
    challenge_match.blackbriar = challengee_strategy
    challenge_match.save()
    challenge.save(update_fields=['state'])
    return challenge


def determine_challenge_winner(challenge_id):
    challenge = app_models.Challenge.objects.get(id=challenge_id, state=app_models.Challenge.COMPLETED)
    winner = challenge.match.winner
    return winner


def match_result(match):
    war_stats = skirmish_result(match.hitmen, match.blackbriar)
    winner = determine_winner(war_stats)
    return war_stats, winner


def make_strategy(gamer, strategy_map):
    strategy = app_models.Strategy(player=gamer, grid=strategy_map)
    strategy.save()
    return strategy


def skirmish_result(hitmen_strategy, blackbriar_strategy):
    survivor = lambda hitmen, blackbriar: hitmen_strategy.player if blackbriar in hitmen.can_kill.all()\
        else blackbriar_strategy.player
    soldier = lambda pk: app_models.Soldier.objects.get(pk=pk)
    shootout = [
        survivor(soldier(hitmen), soldier(blackbriar)) for (hitmen_pos, hitmen), (blackbriar_pos, blackbriar) in zip(
            hitmen_strategy.grid.items(), blackbriar_strategy.grid.items())
    ]
    return Counter(shootout)


def determine_winner(war_stats):
    return max(war_stats.iterkeys(), key=lambda k: war_stats[k])


def get_active_user_profile(request):
    return request.user.abs_profile
