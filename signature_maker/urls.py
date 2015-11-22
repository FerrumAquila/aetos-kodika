from django.conf.urls import url

import views as app_views

urlpatterns = [
    # html view urls
    url(r'^home/$', app_views.index, name='sm_home'),
    url(r'^$', app_views.index, name='sm_home'),
]
