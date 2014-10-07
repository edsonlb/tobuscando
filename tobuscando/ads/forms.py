# coding: utf-8
from django import forms
from .models import Ad, Offer, Category, CategoryMeta, MetaOption


class AdForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AdForm, self).__init__(*args, **kwargs)
        self.fields['link_reference'].widget = forms.TextInput(attrs={
            'placeholder': 'Link se já encontrou algo parecido na Internet...'})
        #self.fields['limit_date'].widget = forms.DateField(format=('%d/%m/%y'),
         #                                                   attrs={})

    class Meta:
        model = Ad
        exclude = ('person', 'slug', 'is_active')
        widgets = {
            'price': forms.TextInput(),

        }

class AdUpdateForm(forms.ModelForm):

    class Meta:
        model = Ad
        fields = (
            'image', 'category', 'title', 'price', 'description',
            'link_reference', 'limit_date', 'view_phone', 'is_bargain'
        )

class OfferForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)

        self.fields['link'].required = False

    class Meta:
        model = Offer
        exclude = ('is_active',)
        widgets = {
            'link': forms.TextInput(attrs={
                'placeholder': 'http://tobuscando/seuproduto'
            }),
            'price': forms.TextInput(),
            'ad': forms.HiddenInput(),
            'person': forms.HiddenInput(),
            'parent': forms.HiddenInput(),
        }


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
        label = '%s:' % self.instance.meta.name

        self.fields['meta'].widget.attrs['class'] = 'hide'

        if self.instance.meta.field in ['text', 'textarea']:
            self.fields['options'] = forms.CharField(label=label,
                                                     required=False)
        else:
            self.fields['options'] = forms.ModelChoiceField(
                label=label, required=False, queryset=option_list)

        if self.instance.meta.field == 'textarea':
            self.fields['options'].widget = forms.TextareaInput(label=label)

        if self.instance.meta.field == 'checkbox':
            self.fields[
                'options'].widget = forms.CheckboxSelectMultiple(label=label)

        if self.instance.meta.field == 'radio':
            self.fields['options'].widget = forms.RadioSelectMultiple(
                label=label)

        if self.instance.meta.field == 'date':
            self.fields['options'] = forms.DateField(label=label,
                                                     required=False)
        if self.instance.meta.field == 'datetime':
            self.fields['options'] = forms.DateTimeField(
                label=label, required=False)

    class Meta:
        model = CategoryMeta
        fields = ('meta', 'options')


CategoryMetaInlineFormset = forms.models.inlineformset_factory(
    Category, CategoryMeta,
    form=CategoryMetaFormInline,
    extra=0,
    can_delete=False
)
