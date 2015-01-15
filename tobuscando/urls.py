# coding: utf-8
from django.conf.urls import patterns, include, url, static
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^accounts/', include('allauth.urls')),
    url(r'^dashboard/', include('tobuscando.dashboard.urls', namespace='dashboard')),
    url(r'^anuncios/', include('tobuscando.ads.urls', namespace='ads')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('tobuscando.core.urls', namespace='core')),
)

#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
