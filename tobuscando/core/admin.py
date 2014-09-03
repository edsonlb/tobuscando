from django.contrib import admin
from .models import Person
from .models import Contact


admin.site.register(Person)
admin.site.register(Contact)
