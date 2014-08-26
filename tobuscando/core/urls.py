# coding: utf-8
from django.conf.urls import patterns, url
from .views import HomeView, SearchView


urlpatterns = patterns('tobuscando.core.views',
    url(r'^busca/(?P<slug>[\w_-]+)/$',
        SearchView.as_view(), name='search'),
    url(r'^$', HomeView.as_view(), name='home'),
    #url(r'^products/$', ProductView.as_view(), name='products'),
)
