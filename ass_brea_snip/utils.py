# coding=utf-8
from django.contrib.auth.decorators import user_passes_test

__author__ = 'ironeagle'

import math

from . import models as abs_models


# TODO: make general matrix class and use that as parent for SectorMap
class SectorMap(object):
    """
    Test

    data = [[0,1,0], [1,0,0], [0,0,1]]
    sector_map = ass_utils.SectorMap(data)
    old_map = sector_map.get_map_json()
    new_sector_map = ass_utils.SectorMap(old_map)
    if new_sector_map.get_map_json() == old_map:
        print 'great success!!!!'
    else:
        print 'great success!!!......not'
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

    def get_map_json(self):
        return {'%s__%s' % (x, y): self.data[x][y] for x, row in enumerate(self.data) for y, r in enumerate(row)}


def abs_profile_required(view_func):
    def test_func(user):
        try:
            user.abs_profile
        except abs_models.UserProfile.DoesNotExist:
            return False
        else:
            return True
    return user_passes_test(test_func=test_func)(view_func)


def get_or_create_challenge(challenger, challengee, match_id):
    return abs_models.Challenge.objects.get_or_create(
        challenger=challenger, challengee=challengee, match=match_id
    )


def accept_challenge(challenge_id):
    challenge = abs_models.Challenge.objects.get(id=challenge_id)
    challenge.state = abs_models.Challenge.ACCEPTED
    challenge.save(update_fields=['state'])
    return challenge


def decline_challenge(challenge_id):
    challenge = abs_models.Challenge.objects.get(id=challenge_id)
    challenge.state = abs_models.Challenge.DECLINED
    challenge.save(update_fields=['state'])
    return challenge
