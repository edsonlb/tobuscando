# coding: utf-8
from django.conf.urls import url, patterns
from .views import (AdCreateView, AdDetailView, OfferCreateView,
                    CategoryDetailView, CategoryListView, CategoryMetaView,
                    AdCreateSuccessTemplateView)


urlpatterns = patterns('tobuscando.ads.views',
    url(r'^category_meta/(?P<pk>\d+)/$', CategoryMetaView.as_view(),
        name="ad_create"),
    url(r'^successo/$', AdCreateSuccessTemplateView.as_view(),
        name="ad_success"),
    url(r'^novo/$', AdCreateView.as_view(), name="ad_create"),
    url(r'^categorias/(?P<slug>[\w_-]+)/$', CategoryDetailView.as_view(),
        name="category_detail"),
    url(r'^categorias/$', CategoryListView.as_view(), name="category_list"),
    url(r'^offer/$', OfferCreateView.as_view(), name="offer_create"),
    url(r'^(?P<slug>[\w_-]+)/$', AdDetailView.as_view(), name="ad_detail"),
)
