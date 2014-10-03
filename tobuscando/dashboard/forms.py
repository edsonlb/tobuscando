# coding: utf-8
from django import forms
from django.utils.translation import ugettext as _
from tobuscando.core.models import Person
from tobuscando.ads.models import Offer


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].label = _(u'Nome')
        self.fields['username'].help_text = None


    class Meta:
        model = Person
        fields = (
            'avatar', 'first_name', 'username', 'email', 'phone', 'cellphone',
            'zipcode', 'address', 'number', 'district', 'city', 'state', 'country',
            'language', 'facebook_link', 'twitter_link', 'gplus_link',
            'notification1', 'notification2', 'notification3', 'notification4',
            'date_joined', 'last_login', 'password'
        )

        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.TextInput(attrs={'readonly': 'readonly'}),
            'password': forms.HiddenInput(),
            'last_login': forms.HiddenInput(),
            #'date_joined': forms.HiddenInput()
        }


class OfferResponseForm(forms.ModelForm):

    class Meta:
        model = Offer
        widgets = {
            'parent': forms.HiddenInput(),
            'person': forms.HiddenInput(),
            'ad': forms.HiddenInput(),
        }
