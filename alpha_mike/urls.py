from django.conf.urls import url

from . import views as app_views

urlpatterns = [
    # html view urls
    url(r'^$', app_views.index, name='alpha_mike_home'),
]
