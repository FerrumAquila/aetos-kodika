# coding=utf-8
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic as generic_views
from django.db import models as django_models

from . import models as abs_models
from . import utils as abs_utils


# @login_required
def index(request):
    return render(request, "ass_brea_snip/index.html", {})


class MatchListView(generic_views.ListView):
    model = abs_models.Match

    @method_decorator(abs_utils.abs_profile_required)
    def dispatch(self, request, *args, **kwargs):
        super(MatchListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(
            django_models.Q(hitmen__player__user=self.request.user.id) |
            django_models.Q(blackbriar__player__user=self.request.user.id)
        )
