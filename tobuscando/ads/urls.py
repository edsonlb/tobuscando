# coding: utf-8
from django.conf.urls import url, patterns
from .views import AdCreateView, CategoryMetaView


urlpatterns = patterns('tobuscando.ads.views',
    #
    url(r'ads/category_meta/(?P<pk>\d+)/$', CategoryMetaView.as_view(),
        name="ad_create"),
    url(r'anunciar/$', AdCreateView.as_view(), name="ad_create"),
)