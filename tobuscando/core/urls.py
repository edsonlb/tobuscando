# coding: utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import DashboardView, DashboardAdsView, ProductView, SingleProductView, ProfileView, AdUpdateView

urlpatterns = patterns('tobuscando.core.views',
    #
    url(r'^$', 'home', name='home'),
    url(r'^products/$', ProductView.as_view(), name='products'),

    url(r'^single-product/$', SingleProductView.as_view(), name='single-products'),

    url(r'^dashboard/$', login_required
        (DashboardView.as_view()), name='dashboard'),
    url(r'^dashboard/ads/$', login_required
        (DashboardAdsView.as_view()), name='dashboard_ads'),
    url(r'^dashboard/ads/(?P<pk>\d+)/$', login_required
        (AdUpdateView.as_view()), name='dashboard_ad_edit'),
    url(r'^dashboard/profile/$', login_required
        (ProfileView.as_view()), name='dashboard_profile'),
    #url(r'^register/reminder/$', 'register_reminder', name='register_reminder'),
    #url(r'^register/(?P<token>\d+)/activate/$', 'register_activate', name='register_activate'),
    #url(r'^activation_success/$', 'register_activation_success', name='registeractivation_success'),
    #url(r'^activation_error/$', 'register_activation_error', name='register_activation_error'),

)
