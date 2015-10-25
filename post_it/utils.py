__author__ = 'ironeagle'

from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import User, Profile, Sticky, StickyOnSticky

success_true = lambda extra: {'success': True}.update(extra)
success_false = lambda extra, error, code: {'success': False, 'error': error, 'code': code}.update(extra)


def _is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def sign_up_or_login(email, password):
    password = password

    try_user = User.objects.filter(email=email)
    if not try_user:
        new_username = "%s_%s" % ("".join(email.split("@")[0].split(".")), email.split("@")[1])
        new_email = email
        new_user = User(email=new_email, username=new_username)
        new_user.save()
        new_user.set_password(password)
        new_user.save()

    if _is_valid_email(email):
        try:
            username = User.objects.filter(email=email).values_list('username', flat=True)
        except User.DoesNotExist:
            username = None
        kwargs = {'username': username, 'password': password}

        # noinspection PyBroadException
        try:
            user = authenticate(**kwargs)
        except:
            user = None

        return user
    else:
        return None


def get_desk(profile):
    return [sticky.mini_json() for sticky in Sticky.objects.filter(author=user)]