# coding: utf-8
from django.conf.urls import patterns, include, url, static
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tobuscando.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),

    #url(r'^login/$', 'tobuscando.core.views.login', name='login'),
    #url(r'^login/$', 'tobuscando.core.views.login', name='login'),

    url(r'^', include('tobuscando.ads.urls', namespace='ads')),
    url(r'^', include('tobuscando.core.urls', namespace='core')),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
