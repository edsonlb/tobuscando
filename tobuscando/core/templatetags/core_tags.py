# coding: utf-8
from django import template
from django.utils.text import Truncator, wrap, phone2numeric

from locale import setlocale, currency as moeda, LC_ALL


register = template.Library()


@register.filter
def brl(value):
    #value = float(value.replace('.', '').replace(',', '.'))

    try:
        setlocale(LC_ALL, 'pt_BR.UTF-8')
        preco = moeda(value, grouping=True)

        return preco
    except:
        return ''
