__author__ = 'ironeagle'

import datetime

from django.shortcuts import *


def index(request):
    # from IPython.frontend.terminal.embed import InteractiveShellEmbed
    # InteractiveShellEmbed()()
    with open('am_access.log', 'w+') as f:
        f.write(str(request.__dict__))
        f.write('\n================================================================')
        f.write(str(datetime.datetime.now()))
        f.write('\n================================================================')
    return render(request, "am-index.html", {})

