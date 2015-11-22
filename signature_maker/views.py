__author__ = 'ironeagle'


from django.shortcuts import *
from django.http import *
from .models import Signature

# from IPython.frontend.terminal.embed import InteractiveShellEmbed
# InteractiveShellEmbed()()


def index(request):
    sig_designs = Signature.objects.all()
    return render(request, "signature_maker/index.html", {'sig_designs': sig_designs})

