from django.shortcuts import HttpResponse, render_to_response


def index(request):
    return render_to_response("core/home.html", {})


def home(request):
    return render_to_response("core/home.html", {})


def profile(request):
    return render_to_response("core/profile.html", {})


def common_path(request):
    return render_to_response("core/common-path.html", {})
