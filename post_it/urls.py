from django.conf.urls import url

import views as app_views

urlpatterns = [
    url(r'^follow/$', app_views.follow, name='tc_follow'),
    url(r'^follow/(?P<username>\w+)/$', app_views.follow, name='tc_follow'),
    url(r'^home/$', app_views.home, name='tc_home'),
    url(r'^landing_page/$', app_views.landing_page, name='tc_landing_page'),
    url(r'^login/$', app_views.login, name='tc_login'),
    url(r'^like_tweet/$', app_views.like_tweet, name='tc_like_tweet'),
    url(r'^like_tweet/(?P<tweet_id>\w+)/$', app_views.like_tweet, name='tc_like_tweet'),
    url(r'^timeline/(?P<username>\w+)/$', app_views.timeline, name='tc_timeline'),
    url(r'^timeline/$', app_views.timeline, name='tc_timeline'),
    url(r'^profile/$', app_views.profile, name='tc_profile'),
    url(r'^post_tweet/$', app_views.post_tweet, name='tc_post_tweet'),
    url(r'^reply_tweet/$', app_views.reply_tweet, name='tc_reply_tweet'),
    url(r'^reply_tweet/(?P<tweet_id>\w+)/$', app_views.reply_tweet, name='tc_reply_tweet'),
    url(r'^tweet/$', app_views.tweet, name='tc_tweet'),
    url(r'^tweet/(?P<tweet_id>\w+)/$', app_views.tweet, name='tc_tweet'),
    url(r'^$', app_views.home, name='home'),
]
