# coding=utf-8
from . import forms as abs_forms
from . import utils as abs_utils
from . import models as abs_models
from aetos.project_utils import utils as aetos_utils

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


# @login_required
def index(request):
    return render(request, "ass_brea_snip/index.html", {})


# @login_required
@csrf_exempt
def challenge_player(request, blackbrair):
    challenge_form = abs_forms.ChallengePlayer(request=request, blackbrair=blackbrair)
    return JsonResponse(challenge_form.save())


# @login_required
@csrf_exempt
def accept_challenge(request, challenge_id):
    challenge_id = abs_utils.accept_challenge(challenge_id)
    return JsonResponse(aetos_utils.success_true({'challenge_id': challenge_id}))


# @login_required
@csrf_exempt
def decline_challenge(request, challenge_id):
    challenge_id = abs_utils.decline_challenge(challenge_id)
    return JsonResponse(aetos_utils.success_true({'challenge_id': challenge_id}))


# @login_required
@csrf_exempt
def fight_challenge(request, challenge_id):
    challenge_form = abs_forms.FightChallenge(request=request, challenge_id=challenge_id)
    return JsonResponse(challenge_form.save())


# @login_required
@csrf_exempt
def challenge_result(request, challenge_id):
    challenge = abs_models.Challenge.objects.get(pk=challenge_id)
    return JsonResponse(abs_utils.json_match_result(challenge.match.result))
