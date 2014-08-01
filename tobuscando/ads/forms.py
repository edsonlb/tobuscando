# coding: utf-8
from django import forms
from .models import Ad, CategoryMeta, MetaOption


class CategoryMetaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CategoryMetaForm, self).__init__(*args, **kwargs)

        try:
            self.fields['options'].queryset = MetaOption.objects.filter(
                meta=self.instance.meta).order_by('order')
        except:
            self.fields['options'].queryset = MetaOption.objects.filter(
                is_active=False).order_by('order')

    class Meta:
        model = CategoryMeta


class AdForm(forms.ModelForm):

    class Meta:
        model = Ad
        exclude = ('slug', 'is_active',)
