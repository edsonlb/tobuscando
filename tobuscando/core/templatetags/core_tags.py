# coding: utf-8
from django import template
from locale import setlocale, currency as moeda, LC_ALL


register = template.Library()


@register.filter
def brl(value):
    try:
        setlocale(LC_ALL, 'pt_BR.UTF-8')
        preco = moeda(value, grouping=True)

        return preco
    except:
        return ''
