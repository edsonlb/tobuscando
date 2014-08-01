# coding: utf-8
from django.conf.urls import url, patterns
from .views import AdCreateView


urlpatterns = patterns('tobuscando.ads.views',
    #
    url(r'novo/$', AdCreateView.as_view()),
)
