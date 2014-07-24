# coding: utf-8
from django.db import models
from django.utils.translate import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField


class Person(AbstractUser):
    # username
    # first_name
    # last_name
    # email
    # password
    # is_staff
    # is_active
    # is_superuser
    # last_login
    # date_joined
    address = models.CharField(_(u'endereço'), max_length=100, blank=True)
    number = models.IntegerField(_(u'número'), blank=True)
    district = models.CharField(_(u'bairro'), max_length=100, blank=True)
    city = models.CharField(_(u'cidade'),max_length=100, blank=True)
    state = models.CharField(_(u'estado'), max_length=2, blank=True)
    country = models.CharField(_(u'país'), max_length=60, blank=True)
    zipcode = models.CharField(_(u'cep'), max_length=10, blank=True)
    language = models.CharField(_(u'idioma'), max_length=10, blank=True)
    avatar = CloudinaryField(_(u'foto'))
    facebook_link = models.CharField(_(u'facebook link'), max_length=100, blank=True)
    twitter_link = models.CharField(_(u'twitter link'), max_length=100, blank=True)
    gplus_link = models.CharField(_(u'google plus'), max_length=100, blank=True)

    class Meta:
        verbose_name = _(u'Pessoa')
        verbose_name_plural = _(u'Pessoas')

    def __unicode__(self):
        return u'{username} ({email})'.format(username=self.username, email=self.email)
