# coding: utf-8
from django import template
from django.template.loader import render_to_string
from tobuscando.ads.models import Category


register = template.Library()


@register.simple_tag
def categories():
    return 'html'
