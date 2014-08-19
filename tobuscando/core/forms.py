# coding: utf-8
from django import forms
from tobuscando.core.models import Person
from django.contrib.auth.forms import UserCreationForm


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


class PersonPreRegisterForm(UserCreationForm):

    terms = forms.BooleanField(label=u'Estou ciente e de acordo com os Termos de Uso.')

    class Meta:
        model = Person
        fields = ('first_name', 'username', 'email', 'password1', 'password2', 'terms')
