from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tobuscando.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'tobuscando.core.views.home', name='home'),

    #urls allauth
    (r'^accounts/', include('allauth.urls')),
    #url(r'^login/$', 'tobuscando.core.views.login', name='login'),
    #url(r'^login/$', 'tobuscando.core.views.login', name='login'),

    url(r'^', include('tobuscando.ads.urls', namespace='ads')),
    url(r'^', include('tobuscando.core.urls', namespace='core')),
)
