# coding: utf-8
from django import forms
from .models import Ad, Category, CategoryMeta, MetaOption


class AdForm(forms.ModelForm):

    class Meta:
        model = Ad
        exclude = ('slug', 'is_active')


class CategoryMetaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CategoryMetaForm, self).__init__(*args, **kwargs)

        try:
            self.fields['options'].queryset = MetaOption.objects.filter(
                meta=self.instance.meta).order_by('order')
        except:
            self.fields['options'].queryset = MetaOption.objects.filter(
                is_active=True).order_by('order')

    class Meta:
        model = CategoryMeta


class CategoryMetaFormInline(forms.ModelForm):

    instance = None

    def __init__(self, *args, **kwargs):
        super(CategoryMetaFormInline, self).__init__(*args, **kwargs)

        option_list = self.instance.options.all()

        self.fields['meta'].label = self.instance.meta.name
        self.fields['meta'].widget.attrs['class'] = 'hide'

        self.fields['options'].label = ''

        if self.instance.meta.field in ['text', 'textarea']:
            self.fields['options'] = forms.CharField(required=False)
        else:
            self.fields['options'] = forms.ModelChoiceField(
                required=False, queryset=option_list)

        if self.instance.meta.field == 'textarea':
            self.fields['options'].widget = forms.TextareaInput()

        if self.instance.meta.field == 'checkbox':
            self.fields['options'].widget = forms.CheckboxSelectMultiple()

        if self.instance.meta.field == 'radio':
            self.fields['options'].widget = forms.RadioSelectMultiple()

        if self.instance.meta.field == 'date':
            self.fields['options'] = forms.DateField(label='', required=False)
        if self.instance.meta.field == 'datetime':
            self.fields['options'] = forms.DateTimeField(label='', required=False)

    class Meta:
        model = CategoryMeta
        fields = ('meta', 'options')


CategoryMetaInlineFormset = forms.models.inlineformset_factory(
    Category, CategoryMeta,
    form=CategoryMetaFormInline,
    extra=0,
    can_delete=False
)
