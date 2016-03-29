__author__ = 'ironeagle'
import json

from . import models as abs_models
from . import utils as abs_utils

from django import forms
from core.project_utils import utils as aetos_utils


class ChallengePlayer(forms.Form):

    def __init__(self, request, blackbriar):
        super(ChallengePlayer, self).__init__()
        self.request = request
        post_data = json.loads(self.request.POST['post_data'])
        hitmen = post_data['hitmen_gamer_tag']
        hitmen_strategy_grid = post_data['hitmen_strategy_grid']
        """hitmen_strategy_grid = {
            '0__0': 2,
            '0__1': 1,
            '0__2': 2,
            '1__0': 1,
            '1__1': 2,
            '1__2': 2,
            '2__0': 2,
            '2__1': 2,
            '2__2': 1
        }"""
        self.hitmen = abs_models.UserProfile.objects.get(user=self.request.user, gamer_tag=hitmen)
        self.blackbriar = abs_models.UserProfile.objects.get(gamer_tag=blackbriar)
        self.hitmen_strategy = abs_utils.make_strategy(self.hitmen, hitmen_strategy_grid)
        match = abs_models.Match(hitmen=self.hitmen_strategy)
        match.save()
        self.challenge, created = abs_utils.get_or_create_challenge(self.hitmen, self.blackbriar, match.id)

    def save(self):
        response = aetos_utils.success_true({'challenge_id': self.challenge.id})
        return response


class FightChallenge(forms.Form):

    def __init__(self, request, challenge_id):
        super(FightChallenge, self).__init__()
        self.request = request
        post_data = json.loads(self.request.POST['post_data'])
        blackbriar_strategy_grid = post_data['blackbriar_strategy_grid']
        """blackbriar_strategy_grid = {
            '0__0': 1,
            '0__1': 2,
            '0__2': 1,
            '1__0': 2,
            '1__1': 1,
            '1__2': 1,
            '2__0': 1,
            '2__1': 1,
            '2__2': 2
        }"""
        self.challenge = abs_models.Challenge.objects.get(pk=challenge_id)
        self.hitmen = self.challenge.challenger
        self.blackbriar = self.challenge.challengee
        self.blackbriar_strategy = abs_utils.make_strategy(self.blackbriar, blackbriar_strategy_grid)

    def save(self):
        abs_utils.accept_challenge(self.challenge.id)
        abs_utils.fight_challenge(self.challenge.id, self.blackbriar_strategy.grid)
        result = self.challenge.match.result
        response = aetos_utils.success_true(abs_utils.json_match_result(result))
        return response

