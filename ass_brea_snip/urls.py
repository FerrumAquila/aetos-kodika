from django.conf.urls import url

import views as app_views

urlpatterns = [
    # json view urls

    # api urls

    # html view urls
    url(r'^home/$', app_views.index, name='abs_home'),
]
