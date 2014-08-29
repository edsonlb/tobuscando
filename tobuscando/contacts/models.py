from django.db import models

# Create your models here.

from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Contact(models.Model):
        full_name = models.CharField(_('nome completo'), max_length=100)
        email = models.EmailField(_('email'))
        phone = models.CharField(_('telefone'), max_length=20, blank=True)
        message = models.TextField(_('mensagem'), max_length=500)

        class Meta:
            verbose_name = _(u'contato')
            verbose_name_plural = _(u'contatos')

        def __unicode__(self): return self.full_name