__author__ = 'ironeagle'


from django.shortcuts import *


def index(request):
    return render(request, "common_path/cp-index.html", {})

