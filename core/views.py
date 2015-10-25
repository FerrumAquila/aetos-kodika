from django.shortcuts import HttpResponse, render_to_response


def profile(request):
    return render_to_response("core/profile.html", {})
