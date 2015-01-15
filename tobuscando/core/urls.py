# coding: utf-8
from django.conf.urls import patterns, url
from django.contrib.flatpages.views import flatpage
from .views import HomeView, SearchView, PersonAdView


urlpatterns = patterns('tobuscando.core.views',
	url(r'busca/$', SearchView.as_view(), name='search'),
    url(r'busca/(?P<slug>[\w_-]+)/$', SearchView.as_view(), name='search'),
    url(r'pages/(?P<url>.*/)$', flatpage, name='flatpage'),
    url(r'contato/$', 'contact', name='contact'),
    url(r'person/(?P<username>[\w_-]+)/$', PersonAdView.as_view(), name="person_view"),
    url(r'^$', HomeView.as_view(), name='home'),
)
