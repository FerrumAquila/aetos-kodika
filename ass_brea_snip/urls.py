from django.conf.urls import url

import views as app_views

urlpatterns = [
    # json view urls
    url(r'^challenge/fight/(?P<challenge_id>[\w-]+)/$', app_views.fight_challenge, name='abs_fight_challenge'),
    url(r'^challenge/accept/(?P<challenge_id>[\w-]+)/$', app_views.accept_challenge, name='abs_accept_challenge'),
    url(r'^challenge/decline/(?P<challenge_id>[\w-]+)/$', app_views.decline_challenge, name='abs_decline_challenge'),
    url(r'^challenge/(?P<blackbrair>[\w-]+)/$', app_views.challenge_player, name='abs_challenge_player'),

    # api urls

    # html view urls
    url(r'^home/$', app_views.index, name='abs_home'),
]
