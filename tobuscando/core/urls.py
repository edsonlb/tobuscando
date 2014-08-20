# coding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('tobuscando.core.views',
    #url(r'^login/$', 'login', name='login'),
    #url(r'^login/validate/$', 'login_validate', name='login'),
    #url(r'^logoff/$', 'logoff', name='logoff'),
    #url(r'^dashboard/$', 'dashboard_index', name='dashboard_index'),
    #url(r'^register/$', 'register_form', name='register_form'),
    #url(r'^register/validate/$', 'register_validate', name='register_validate'),
    #url(r'^register/reminder/$', 'register_reminder', name='register_reminder'),
    #url(r'^register/(?P<token>\d+)/activate/$', 'register_activate', name='register_activate'),
    #url(r'^activation_success/$', 'register_activation_success', name='registeractivation_success'),
    #url(r'^activation_error/$', 'register_activation_error', name='register_activation_error'),

)
"""
urlpatterns += patterns('',
    #url(r'^reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'tobuscando.core.views.reset_confirm', name='reset_confirm'),
    url(r'^reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'tobuscando.core.views.reset_confirm', {'template_name': 'password/password_reset_confirm.html'}, name='reset_confirm'),
    url(r'^reset/$', 'tobuscando.core.views.reset', name='reset'),
    #url(r'^user/password/reset/$','django.contrib.auth.views.password_reset', {'post_reset_redirect' : '/user/password/reset/done/', 'template_name': 'password/password_reset_form.html'}, name="password_reset"),
    #url(r'^user/password/reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'password/password_reset_done.html'}),
    #url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'post_reset_redirect' : '/user/password/done/', 'template_name': 'password/password_reset_confirm.html'}, name='password_reset_confirm'),
    #url(r'^user/password/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'password/password_reset_complete.html'}),
)

#http://catherinetenajeros.blogspot.com.br/2013/03/password-reset.html
#http://blog.xjtian.com/post/54552214875/built-in-password-reset-views-in-django
#http://garmoncheg.blogspot.com.br/2012/07/django-resetting-passwords-with.html
#https://github.com/django/django/tree/master/django/contrib/admin/templates/registration
"""