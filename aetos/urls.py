from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login, logout

admin.autodiscover()

urlpatterns = [
    url(r'', include('core.urls')),
    url(r'^post-it/', include('post_it.urls')),
    url(r'^signature-maker/', include('signature_maker.urls')),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout, {'next_page': '/'}),
] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
