from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tobuscando.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^anuncio/', include('tobuscando.ads.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
