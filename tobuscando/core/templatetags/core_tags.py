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


@register.filter(is_safe=True)
@stringfilter
def truncatechars_html(value, arg):
    """
    Truncates HTML after a certain number of chars.

    Argument: Number of chars to truncate after.

    Newlines in the HTML are preserved.
    """
    try:
        length = int(arg)
    except ValueError:  # invalid literal for int()
        return value  # Fail silently.
    return Truncator(value).chars(length, html=True)
