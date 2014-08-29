# coding: utf-8
from django import forms
from tobuscando.contacts.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact