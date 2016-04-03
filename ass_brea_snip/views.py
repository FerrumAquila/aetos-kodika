# coding=utf-8
import json
from . import forms as abs_forms
from . import utils as abs_utils
from . import models as abs_models
from core.project_utils import utils as aetos_utils

from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# TODO: get_active_user_profile should be added to request
@login_required
def index(request):
    challenges = [challenge.mini_json for challenge in abs_utils.open_challenge_list(abs_utils.get_active_user_profile(request))]
    return render(request, "ass_brea_snip/index.html", {
        'hitmen_profile': abs_utils.get_active_user_profile(request),
        'id_icon_map': json.dumps(abs_models.Soldier.objects.id_icon_map()),
        'challenges': challenges,
        'gamer_profiles': abs_models.UserProfile.objects.all()  #.exclude(user=request.user),
    })


# TODO: get_active_user_profile should be added to request
@login_required
def load_grid(request):
    rendered_html = render(request, "ass_brea_snip/components/grid.html", {})
    return JsonResponse(aetos_utils.success_true({'rendered_html': str(rendered_html)}))


@login_required
@csrf_exempt
def challenge_player(request, blackbriar):
    challenge_form = abs_forms.ChallengePlayer(request=request, blackbriar=blackbriar)
    return JsonResponse(challenge_form.save())


@login_required
@csrf_exempt
def accept_challenge(request, challenge_id):
    challenge_id = abs_utils.accept_challenge(challenge_id)
    return JsonResponse(aetos_utils.success_true({'challenge_id': challenge_id}))


@login_required
@csrf_exempt
def decline_challenge(request, challenge_id):
    challenge_id = abs_utils.decline_challenge(challenge_id)
    return JsonResponse(aetos_utils.success_true({'challenge_id': challenge_id}))


@login_required
@csrf_exempt
def fight_challenge(request, challenge_id):
    challenge_form = abs_forms.FightChallenge(request=request, challenge_id=challenge_id)
    return JsonResponse(challenge_form.save())


@login_required
@csrf_exempt
def challenge_result(request, challenge_id):
    challenge = abs_models.Challenge.objects.get(pk=challenge_id)
    return JsonResponse(abs_utils.json_match_result(challenge.match.result))


@login_required
@csrf_exempt
def open_challenges(request):
    challenges = [challenge.mini_json for challenge in abs_utils.open_challenge_list(abs_utils.get_active_user_profile(request))]
    return JsonResponse(aetos_utils.success_true({'challenges': challenges}))
