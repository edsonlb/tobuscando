# coding: utf-8
from django import forms
from django.utils.translation import ugettext as _
from tobuscando.core.models import Person


class PersonForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)

        self.fields['last_login'].widget = forms.HiddenInput()
        self.fields['date_joined'].widget = forms.HiddenInput()

    class Meta:
        model = Person


class LoginForm(forms.Form):
    username = forms.CharField(max_length='200', required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class PersonPreRegisterForm(forms.ModelForm):
    terms = forms.BooleanField(
        label=u'Estou ciente e de acordo com os Termos de Uso.')

    def __init__(self, *args, **kwargs):
        super(PersonPreRegisterForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True

    class Meta:
        model = Person
        fields = ('first_name', 'username', 'email', 'password', 'terms')
        widget = {
            'password': forms.PasswordInput()
        }


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].label = _(u'Nome')
        self.fields['username'].help_text = None
        self.fields['username'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

        self.fields['password'].widget = forms.HiddenInput()
        self.fields['last_login'].widget = forms.HiddenInput()
        self.fields['date_joined'].widget = forms.HiddenInput()

    class Meta:
        model = Person
        fields = (
            'avatar', 'first_name', 'username', 'email',
            'zipcode', 'address', 'number', 'district', 'city', 'state', 'country',
            'language', 'facebook_link', 'twitter_link', 'gplus_link',
            'notification1', 'notification2', 'notification3', 'notification4',
            'date_joined', 'last_login', 'password'
        )
