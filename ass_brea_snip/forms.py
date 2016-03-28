__author__ = 'ironeagle'
from . import models as abs_models
from . import utils as abs_utils

from django import forms
from aetos.project_utils import utils as aetos_utils


class ChallengePlayer(forms.Form):
    hitmen = forms.CharField(max_length=255)
    blackbrair = forms.CharField(max_length=255)
    hitmen_grid = forms.CharField(max_length=2048)

    def __init__(self, request, blackbrair):
        super(ChallengePlayer, self).__init__()
        self.request = request
        hitmen = self.request.POST['hitmen_gamer_tag']
        # hitmen_strategy_grid = self.request.POST['hitmen_strategy_grid']
        hitmen_strategy_grid = {
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
        self.hitmen = abs_models.UserProfile.objects.get(user=self.request.user, gamer_tag=hitmen)
        self.blackbrair = abs_models.UserProfile.objects.get(gamer_tag=blackbrair)
        self.hitmen_strategy = abs_utils.make_strategy(self.hitmen, hitmen_strategy_grid)
        match = abs_models.Match(hitmen=self.hitmen_strategy)
        match.save()
        self.challenge, created = abs_utils.get_or_create_challenge(self.hitmen, self.blackbrair, match.id)

    def save(self):
        response = aetos_utils.success_true({'challenge_id': self.challenge.id})
        return response

