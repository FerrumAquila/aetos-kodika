from django.conf.urls import url

import views as app_views

urlpatterns = [
    # api call urls
    url(r'^api/signature_html/get/(?P<sid>[\d-]+)/$', app_views.get_signature_html, name='sm_api_get_sig_html'),

    # html view urls
    url(r'^home/$', app_views.index, name='sm_home'),
    url(r'^$', app_views.index, name='sm_home'),
]
