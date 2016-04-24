from django.conf.urls import url

from . import views as app_views

urlpatterns = [
    # html view urls
    url(r'^$', app_views.index, name='web_render_home'),

    # ajax view urls
    url(r'^get-html/$', app_views.get_html, name='web_render_get_html'),

    # ajax view urls
    url(r'^save-image/$', app_views.save_image, name='web_render_save_image'),
]
