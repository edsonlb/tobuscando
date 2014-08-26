# coding: utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from .views import DashboardView, DashboardAdsView, ProfileView, AdUpdateView


urlpatterns = patterns('tobuscando.dashboard.views',
    url(r'^ads/(?P<pk>\d+)/$', login_required
        (AdUpdateView.as_view()), name='ad_edit'),
    url(r'^ads/$', login_required
        (DashboardAdsView.as_view()), name='ad_list'),
    url(r'^profile/$', login_required
        (ProfileView.as_view()), name='profile'),
    url(r'^$', login_required
        (DashboardView.as_view()), name='dash_home'),
)
