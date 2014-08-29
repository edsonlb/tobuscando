# coding: utf-8
from django import forms
from tobuscando.core.models import Person, Contact

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

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact