# coding: utf-8
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext_lazy as _
from cloudinary.models import CloudinaryField
from tobuscando.core.utils import slug


class Category(MPTTModel):
    HELP_IMAGE = _(u'Imagem utilizada como padrão\
                     para anúnicos sem imagem')

    parent = TreeForeignKey('self', verbose_name=_(u'parente'),
                            blank=True, null=True, related_name='children')
    name = models.CharField(_(u'nome'), max_length=50, unique=True)
    slug = models.SlugField(_(u'slug'), blank=True, null=True)
    image = CloudinaryField(_(u'imagem'), blank=True, null=True,
                            help_text=HELP_IMAGE)
    order = models.PositiveIntegerField()
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

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        Category.objects.rebuild()

    @models.permalink
    def get_absolute_url(self):
        return ('')


class Meta(models.Model):
    FIELD_CHOICES = (
        ('text', _(u'Caixa de texto')),
        ('textarea', _(u'Campo de texto')),
        ('select', _(u'Caixa de seleção')),
        ('checkbox', _(u'Caixa de checagem')),
    )

    name = models.CharField(_(u'nome'), max_length=50)
    field = models.CharField(_(u'tipo do campo'), max_length=10,
                             choices=FIELD_CHOICES)
    is_active = models.BooleanField(_(u'ativo?'), default=True)
    created_at = models.DateTimeField(_(u'criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_(u'alterado em'), auto_now=True)

    class Meta:
        verbose_name = _(u'Campo Personalizado')
        verbose_name_plural = _(u'Campos Personalizados')

    def __unicode__(self):
        return self.name

    def save(self):
        pass

    @models.permalink
    def get_absolute_url(self):
        return ('')

    # TODO: Defne custom methods here


""" Signals """


def category_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slug(instance, sender, instance.name)

models.signals.pre_save.connect(category_pre_save, sender=Category)
