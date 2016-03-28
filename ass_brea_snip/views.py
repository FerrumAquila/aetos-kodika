# coding=utf-8
from . import forms as abs_forms

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
