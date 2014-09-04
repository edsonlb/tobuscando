# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, User
from cloudinary.models import CloudinaryField
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialLogin


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
    address = models.CharField(_(u'endereço'), max_length=100,
                               blank=True, null=True)
    number = models.IntegerField(_(u'número'), blank=True, null=True)
    district = models.CharField(_(u'bairro'), max_length=100,
                                blank=True, null=True)
    city = models.CharField(_(u'cidade'), max_length=100, blank=True, null=True)
    state = models.CharField(_(u'estado'), max_length=2, blank=True, null=True)
    country = models.CharField(_(u'país'), max_length=60, blank=True, null=True)
    zipcode = models.CharField(_(u'cep'), max_length=10, blank=True, null=True)
    language = models.CharField(_(u'idioma'), max_length=10,
                                blank=True, null=True)
    avatar = CloudinaryField(_(u'foto'), default='avatar.jpg',
                             blank=True, null=True)
    facebook_link = models.CharField(_(u'facebook link'), max_length=100,
                                     blank=True, null=True)
    twitter_link = models.CharField(_(u'twitter link'), max_length=100,
                                    blank=True, null=True)
    gplus_link = models.CharField(_(u'google plus'), max_length=100,
                                  blank=True, null=True)
    notification1 = models.BooleanField(_(u'notificar anúncio'),
                                        default=True, blank=True)
    notification2 = models.BooleanField(_(u'notificar resposta'),
                                        default=True, blank=True)
    notification3 = models.BooleanField(_(u'notificar celular'),
                                        default=True, blank=True)
    notification4 = models.BooleanField(_(u'notificar rede social'),
                                        default=True, blank=True)
    validation = models.BooleanField(_(u'validação'), default=False, blank=True)

    # criar pontos por negociação. Como no Mercado Livre.
    # (Verificar com equipe: Cria outra tabela ou cria um campo nesta INTEIRO e controla por ele.)

    class Meta:
        verbose_name = _(u'Pessoa')
        verbose_name_plural = _(u'Pessoas')
        ordering = ['email']

    def __unicode__(self):
        return u'{username} ({email})'.format(username=self.username,
                                              email=self.email)

    def ads(self):
        return self.ad_set.all()

    def offers(self):
        return self.offer_set.filter(ad__person=self.pk)

    def get_accounts_facebook(self):
        account_fc = SocialAccount.objects.filter(user_id=self.id)
        return account_fc

class Contact(models.Model):
        full_name = models.CharField(_('nome completo'), max_length=100)
        email = models.EmailField(_('email'))
        phone = models.CharField(_('telefone'), max_length=20, blank=True)
        message = models.TextField(_('mensagem'), max_length=500)

        class Meta:
            verbose_name = _(u'contato')
            verbose_name_plural = _(u'contatos')

        def __unicode__(self): return self.full_name
