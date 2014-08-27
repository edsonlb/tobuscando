# coding: utf-8
from django.conf.urls import url, patterns
from .views import (AdCreateView, AdDetailView,
                    CategoryMetaView, AdCreateSuccessTemplateView)


urlpatterns = patterns('tobuscando.ads.views',
    url(r'^category_meta/(?P<pk>\d+)/$', CategoryMetaView.as_view(),
        name="ad_create"),
    url(r'^anunciar/successo/$', AdCreateSuccessTemplateView.as_view(),
        name="ad_success"),
    url(r'^novo/$', AdCreateView.as_view(), name="ad_create"),
    url(r'^(?P<slug>[\w_-]+)/$', AdDetailView.as_view(), name="ad_detail"),
)
