# coding: utf-8
from django.contrib import admin
from suit.admin import SortableModelAdmin, SortableTabularInline
from mptt.admin import MPTTModelAdmin
from .models import Ad, Category, Meta, MetaOption, CategoryMeta
from .forms import CategoryMetaForm


class MetaOptionTabularInline(SortableTabularInline):
    model = MetaOption

    sortable = 'order'

    def get_extra(self, request, obj=None, **kwargs):
        extra = 1

        if obj:
            extra = 0
        return extra


class MetaAdmin(SortableModelAdmin):
    list_display = ('name', 'field', 'is_active')
    list_filter = ('is_active', 'field')
    search_field = ('name',)

    inlines = [MetaOptionTabularInline]

    sortable = 'order'


class CategoryMetaTabularInline(SortableTabularInline):
    model = CategoryMeta
    form = CategoryMetaForm

    fields = ('meta', 'options', 'is_active', 'order')
    can_delete = False
    filter_vertical = ('options',)

    sortable = 'order'

    def get_extra(self, request, obj=None, **kwargs):
        extra = 1

        if obj:
            extra = 0
        return extra


class CategoryAdmin(MPTTModelAdmin, SortableModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    search_field = ('name', 'slug')
    list_filter = ('is_active', 'parent')

    inlines = [CategoryMetaTabularInline]

    sortable = 'order'

    class Media:
        js = ['admin/js/category.js']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Meta, MetaAdmin)
admin.site.register(Ad)
