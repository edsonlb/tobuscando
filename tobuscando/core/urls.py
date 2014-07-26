# coding: utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('tobuscando.core.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^login/validate/$', 'login_validate', name='login'),
    url(r'^logoff/$', 'logoff', name='logoff'),
    url(r'^dashboard/$', 'dashboard_index', name='dashboard_index'),
    url(r'^register/$', 'register_form', name='register_form'),
    url(r'^register/validate/$', 'register_validate', name='register_validate'),
    url(r'^register/(?P<token>\d+)/activate/$', 'register_activate', name='register_activate'),
    url(r'^activation_success/$', 'register_activation_success', name='registeractivation_success'),
    url(r'^activation_error/$', 'register_activation_error', name='register_activation_error'),

)