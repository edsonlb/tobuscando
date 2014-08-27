# coding: utf-8
from django import template
from locale import setlocale, currency as moeda, LC_ALL


register = template.Library()


@register.filter()
def brl(self):
    try:
        setlocale(LC_ALL, 'pt_BR.UTF-8')
        preco = moeda(self, grouping=True)

        return preco
    except:
        return ''
