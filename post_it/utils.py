__author__ = 'ironeagle'

from django.contrib.auth import authenticate

from .models import *


def _is_valid_email(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError

    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def sign_up_or_login(email, password):
    # username = email
    password = password

    try_user = User.objects.filter(email=email)
    if try_user.count():
        pass
    else:
        new_username = email.split("@")[0]
        stripped_username = ""
        for element in new_username.split("."):
            stripped_username += element
        new_username = stripped_username
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
        try:
            user = authenticate(**kwargs)
        except:
            user = None

        return user
    else:
        return None