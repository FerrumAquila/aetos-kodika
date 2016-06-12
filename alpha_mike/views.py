__author__ = 'ironeagle'

import datetime

from django.shortcuts import *


def index(request):
    with open('am_access.log', 'w+') as f:
        f.write(str(request))
        f.write('\n')
        f.write(str(datetime.datetime.now()))
        f.write('\n')
    return render(request, "am-index.html", {})

