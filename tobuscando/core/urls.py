# coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from .views import HomeView, DashboardView, DashboardAdsView, ProfileView, AdUpdateView


urlpatterns = patterns('tobuscando.core.views',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^dashboard/$', login_required (DashboardView.as_view()),
        name='dashboard'),
    url(r'^dashboard/ads/$', login_required (DashboardAdsView.as_view()),
        name='dashboard_ads'),
    url(r'^dashboard/ads/(?P<pk>\d+)/$', login_required (AdUpdateView.as_view()),
        name='dashboard_ad_edit'),
    url(r'^dashboard/profile/$', login_required (ProfileView.as_view()),
        name='dashboard_profile'),
    url(r'^login/$', 'login', name='login'),
    url(r'^login/validate/$', 'login_validate', name='login'),
    url(r'^logoff/$', 'logoff', name='logoff'),
    url(r'^dashboard/$', 'dashboard_index', name='dashboard_index'),
    url(r'^register/$', 'register_form', name='register_form'),
    url(r'^register/validate/$', 'register_validate', name='register_validate'),
    #url(r'^register/reminder/$', 'register_reminder', name='register_reminder'),
    url(r'^register/(?P<token>\d+)/activate/$', 'register_activate', name='register_activate'),
    url(r'^activation_success/$', 'register_activation_success', name='registeractivation_success'),
    url(r'^activation_error/$', 'register_activation_error', name='register_activation_error'),

)
