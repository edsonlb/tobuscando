from django.contrib import admin
from suit.admin import SortableModelAdmin
from mptt.admin import MPTTModelAdmin
from .models import Category


class CategoryAdmin(MPTTModelAdmin, SortableModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    search_field = ('name', 'slug')
    list_filter = ('parent',)

    mptt_level_indent = 20

    sortable = 'order'

admin.site.register(Category, CategoryAdmin)
