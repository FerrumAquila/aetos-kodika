from django.conf.urls import url

import views as app_views

urlpatterns = [
    # json view urls
    url(r'^profile/$', app_views.profile, name='pt_profile'),
    url(r'^login/$', app_views.login, name='pt_login'),
    url(r'^desk/$', app_views.sticky_desk, name='pt_sticky_desk'),
    url(r'^desk/(?P<username>\w+)/$', app_views.sticky_desk, name='pt_sticky_desk'),

    # api urls
    url(r'^follow/(?P<username>\w+)/$', app_views.follow, name='pt_follow'),
    url(r'^tweet/$', app_views.tweet, name='pt_tweet'),
    url(r'^tweet/(?P<tweet_id>\w+)/$', app_views.tweet, name='pt_reply_tweet'),
    url(r'^tweet/like/(?P<tweet_id>\w+)/$', app_views.like_tweet, name='pt_like_tweet'),

    url(r'^$', app_views.home, name='home'),
]
