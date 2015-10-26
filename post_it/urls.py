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
    url(r'^sticky/$', app_views.sticky, name='pt_sticky'),
    url(r'^sticky/(?P<sticky_id>\w+)/$', app_views.sticky, name='pt_reply_sticky'),
    url(r'^sticky/fav/(?P<sticky_id>\w+)/$', app_views.fav_sticky, name='pt_fav_sticky'),

    # html view urls
    url(r'^home/$', app_views.index, name='pt_home'),
    url(r'^$', app_views.index, name='pt_home'),
]
