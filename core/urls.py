from django.conf.urls import url

import views as app_views

urlpatterns = [
    url(r'^$', app_views.home, name='home'),
]
