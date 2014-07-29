# coding: utf-8
from django import forms
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