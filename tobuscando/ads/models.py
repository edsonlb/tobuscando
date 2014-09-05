# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from cloudinary.models import CloudinaryField
from tobuscando.core.utils import slug


HELP_ORDER = _(u'Utilizado para definir a ordem de exibição no site.')


class Ad(models.Model):
    person = models.ForeignKey('core.Person', verbose_name=_(u'Pessoa'),
                               blank=True, null=True)
    category = TreeForeignKey('Category', verbose_name=_(u'categoria:'))
    title = models.CharField(_(u'título:'), max_length=250)
    slug = models.SlugField(_(u'slug'), blank=True, null=True)
    price = models.CharField(_(u'preço:'), max_length=100)
    description = models.TextField(_(u'descrição:'))
    link_reference = models.URLField(_(u'anúncio de referência:'), blank=True)
    image = CloudinaryField(_(u'imagem:'), blank=True, null=True)
    limit_date = models.DateTimeField(_(u'data limite do anúncio:'),
                                      blank=True, null=True)
    view_phone = models.BooleanField(_(u'exibir telefone no anúncio?'))
    is_bargain = models.BooleanField(_(u'topa negociar?'))
    is_active = models.BooleanField(_(u'ativo?'), default=True)
    created_at = models.DateTimeField(_(u'criado em:'), auto_now_add=True)
    updated_at = models.DateTimeField(_(u'alterado em:'), auto_now=True)

    class Meta:
        verbose_name = _(u'Anúncio')
        verbose_name_plural = _(u'Anúncios')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('ads:ad_detail', (), {'slug': self.slug})

    def offers(self):
        return self.offer_set.filter(parent=None, is_active=True)


class AdMeta(models.Model):
    ad = models.ForeignKey('Ad', related_name='metas',
                           verbose_name=_(u'anúncio'))
    meta = models.ForeignKey('CategoryMeta',
                             related_name='category_meta',
                             verbose_name=_(u'categoria meta'))
    option = models.TextField(_(u'valor'), blank=True)
    is_active = models.BooleanField(_(u'ativo?'), default=True)
    created_at = models.DateTimeField(_(u'criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_(u'alterado em'), auto_now=True)

    class Meta:
        verbose_name = _(u'Anúncio Meta')
        verbose_name_plural = _(u'Anúncios Metas')

    def __unicode__(self):
        return self.ad.title

    def value(self):
        if self.meta.meta.field in ['text', 'textarea', 'date', 'datetime']:
            return self.option

        option = self.meta.options.get(pk=self.option)
        return option


class Category(MPTTModel):
    HELP_IMAGE = _(u'Imagem utilizada como padrão\
                     para anúnicos sem imagem')

    parent = TreeForeignKey('self', verbose_name=_(u'parente'),
                            blank=True, null=True, related_name='children')
    name = models.CharField(_(u'nome'), max_length=50)
    slug = models.SlugField(_(u'slug'), blank=True, null=True)
    image = CloudinaryField(_(u'imagem'), blank=True, null=True,
                            help_text=HELP_IMAGE)
    order = models.PositiveIntegerField(_(u'ordem'), help_text=HELP_ORDER)
    is_active = models.BooleanField(_(u'ativo?'), default=True)
    created_at = models.DateTimeField(_(u'criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_(u'alterado em'), auto_now=True)

    class Meta:
        verbose_name = _(u'Categoria')
        verbose_name_plural = _(u'Categorias')

    class MPTTMeta:
        order_insertion_by = ['order']

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('ads:category_detail', (), {'slug': self.slug})

    def metas(self,):
        return self.categorymeta_set.all()


class Meta(models.Model):
    FIELD_CHOICES = (
        ('text', _(u'Caixa de texto')),
        ('textarea', _(u'Área de texto')),
        ('select', _(u'Selecione')),
        ('checkbox', _(u'Caixa de checagem')),
        ('radio', _(u'Seleção única')),
        ('date', _(u'Data')),
        ('datetime', _(u'Data & Hora')),
    )

    name = models.CharField(_(u'nome'), max_length=100)
    field = models.CharField(_(u'tipo do campo'), max_length=10,
                             choices=FIELD_CHOICES)
    slug = models.SlugField(_(u'slug'), blank=True, null=True)
    order = models.PositiveIntegerField(_(u'ordem'), default=0,
                                        help_text=HELP_ORDER)
    is_active = models.BooleanField(_(u'ativo?'), default=True)
    created_at = models.DateTimeField(_(u'criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_(u'alterado em'), auto_now=True)

    class Meta:
        verbose_name = _(u'Campo Personalizado')
        verbose_name_plural = _(u'Campos Personalizados')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('')


class MetaOption(models.Model):
    meta = models.ForeignKey('Meta', verbose_name=_(u'Meta'))
    value = models.CharField(_(u'valor'), max_length=50)
    order = models.PositiveIntegerField(_(u'ordem'), default=0,
                                        help_text=HELP_ORDER)
    is_active = models.BooleanField(_(u'ativo?'), default=True)
    created_at = models.DateTimeField(_(u'criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_(u'alterado em'), auto_now=True)

    class Meta:
        verbose_name = _(u'Valor Meta')
        verbose_name_plural = _(u'Valores Meta')

    def __unicode__(self):
        return self.value


class CategoryMeta(models.Model):
    category = models.ForeignKey('Category', verbose_name=_(u'categoria'))
    meta = models.ForeignKey('Meta', verbose_name=_(u'meta'))
    options = models.ManyToManyField(MetaOption, verbose_name=_(u'opções'),
                                     blank=True, null=True)
    order = models.PositiveIntegerField(_(u'ordem'), default=0,
                                        help_text=HELP_ORDER)
    is_active = models.BooleanField(_(u'ativo?'), default=True)
    created_at = models.DateTimeField(_(u'criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_(u'alterado em'), auto_now=True)

    class Meta:
        verbose_name = _(u'Campo Personalizado')
        verbose_name_plural = _(u'Campos Personalizados')

    def __unicode__(self):
        return self.meta.name


class Offer(models.Model):
    HELP_LINK = _(u'Link para página ou imagem de produto que está ofertando.')

    ad = models.ForeignKey('Ad', verbose_name=_(u'Anúncio'))
    person = models.ForeignKey('core.Person', verbose_name=_(u'Pessoa'))
    parent = models.ForeignKey('self', verbose_name=_(u'Oferta pai'),
                               null=True, blank=True)
    link = models.URLField(_(u'link do produto'), help_text=HELP_LINK,
                           null=True, blank=True)
    message = models.TextField(_(u'Mensagem'))
    price = models.DecimalField(_(u'preço'), max_digits=5, decimal_places=2)
    is_active = models.BooleanField(_(u'ativo?'), default=False)
    created_at = models.DateTimeField(_(u'criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_(u'alterado em'), auto_now=True)

    class Meta:
        verbose_name = _(u'Oferta')
        verbose_name_plural = _(u'Ofertas')

    def __unicode__(self):
        return u'%s - %s' % (self.ad.title, self.person)

    def relateds(self):
        return Offer.objects.filter(parent=self.pk, is_active=True)


"""
    Signals
"""


def ad_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slug(instance, sender, instance.title)

models.signals.pre_save.connect(ad_pre_save, sender=Ad)


def category_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slug(instance, sender, instance.name)

models.signals.pre_save.connect(category_pre_save, sender=Category)


def meta_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slug(instance, sender, instance.name)

models.signals.pre_save.connect(meta_pre_save, sender=Meta)
