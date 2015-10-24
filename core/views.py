from django.shortcuts import HttpResponse, render_to_response


def home(request):
    # return HttpResponse("WELCOME TO AETOS KODIKA")
    return render_to_response("core/home.html", {})
