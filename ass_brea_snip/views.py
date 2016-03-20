from django.shortcuts import render


# @login_required
def index(request):
    return render(request, "ass_brea_snip/index.html", {})

