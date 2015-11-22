__author__ = 'ironeagle'


from django.shortcuts import *
from django.http import JsonResponse
from .models import Signature
from .forms import SignatureForm

# from IPython.frontend.terminal.embed import InteractiveShellEmbed
# InteractiveShellEmbed()()


def index(request):
    sig_design = Signature.objects.all()[0]
    sig_form = SignatureForm(sig_design)
    return render(request, "signature_maker/index.html", {'sig_design': sig_design, 'sig_form': sig_form})


# TODO: fix this using fhurl
def get_signature_html(request, sid):
    if request.method == 'POST':
        sig_design = Signature.objects.get(pk=sid)
        component_dict = {key.split('id_component_')[1]: request.POST[key] for key in request.POST.keys()
                          if key.startswith('id_component_')}
        component_match = True
        for component in sig_design.components:
            if component not in component_dict.keys():
                component_match = False
        if component_match:
            html = sig_design.html % component_dict
            response = {'success': True, 'message': 'this is message from view in POST', 'html': html}
        else:
            response = {'success': False, 'message': 'this is message from view in no match'}

    else:
        response = {'success': False, 'message': 'this is message from view in GET'}

    return JsonResponse(response)

