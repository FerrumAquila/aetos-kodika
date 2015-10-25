__author__ = 'ironeagle'


from django.shortcuts import *
from django.http import *
from django.contrib.auth import login as auth_login
from django.http import Http404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Profile
from .utils import sign_up_or_login, success_true, success_false
import json
import utils as app_utils

# from IPython.frontend.terminal.embed import InteractiveShellEmbed
# InteractiveShellEmbed()()


@login_required
def profile(request):
    user_profile = Profile.objects.filter(user=request.user)
    if user_profile:
        response = success_true({'user_profile': user_profile[0]})
    else:
        error = 'No profile found for "%s"' % request.user.username
        response = success_false({'user_profile': None}, error, 'not_found')

    return JsonResponse(response)


def login(request):

    login_email = request.POST['login_email']
    login_password = request.POST['login_password']

    user = sign_up_or_login(email=login_email, password=login_password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            response = success_true({'username': user.username})
        else:
            error = '"%s" is not yet activated' % user.username
            response = success_false({'username': user.username}, error, 'inactive')
    else:
        error = '"%s" and "%s" combination is incorrect'
        response = success_false({'username': user.username}, error, 'invalid')

    return JsonResponse(response)


def sticky_desk(request, username=None):
    if not username and request.user.is_authenticated():
        username = request.user.username
    else:
        raise Http404

    # TODO : this is same as def profile. make decorator
    user_profile = Profile.objects.filter(user__username=username)
    if user_profile:
        response = success_true({'user_profile': user_profile[0]})
    else:
        error = 'No profile found for "%s"' % request.user.username
        response = success_false({'user_profile': None}, error, 'not_found')

    response.update({'user_desk': app_utils.get_desk(user_profile[0])})

    return JsonResponse(response)


def follow(request, username=None):
    return JsonResponse(success_false({}, 'API under construction', 'api_not_done'))


def sticky(request, sticky_id=None):
    return JsonResponse(success_false({}, 'API under construction', 'api_not_done'))


def fav_sticky(request, sticky_id):
    return JsonResponse(success_false({}, 'API under construction', 'api_not_done'))


@login_required
def home(request):
    return render(request, "post_it/index.html", {})

