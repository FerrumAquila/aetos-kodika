from django.conf.urls import url

import views as app_views

urlpatterns = [
    url(r'^profile/$', app_views.profile, name='core_profile'),
    url(r'^home/$', app_views.home, name='core_home'),
    url(r'^$', app_views.index, name='core_index'),
]
