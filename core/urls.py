from django.conf.urls import url

import views as app_views

urlpatterns = [
    url(r'^profile/$', app_views.profile, name='core_profile'),
]
