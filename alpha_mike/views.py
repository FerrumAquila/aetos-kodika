__author__ = 'ironeagle'


from django.shortcuts import *


def index(request):
    return render(request, "am-index.html", {})

