# coding: utf-8
from django.contrib import admin
from suit.admin import SortableModelAdmin, SortableTabularInline
from mptt.admin import MPTTModelAdmin
from .models import Ad, AdMeta, Offer, Category, Meta, MetaOption, CategoryMeta
from .forms import CategoryMetaForm


class MetaOptionTabularInline(SortableTabularInline):
    model = MetaOption
    extra = 0

    sortable = 'order'

class MetaAdmin(SortableModelAdmin):
    list_display = ('name', 'field', 'is_active')
    list_filter = ('is_active', 'field')
    search_fields = ('name',)

    inlines = [MetaOptionTabularInline]

    sortable = 'order'


class CategoryMetaTabularInline(SortableTabularInline):
    model = CategoryMeta
    form = CategoryMetaForm
    extra = 0

    fields = ('meta', 'options', 'is_active', 'order')
    can_delete = False
    filter_vertical = ('options',)

    sortable = 'order'


class CategoryAdmin(MPTTModelAdmin, SortableModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    search_fields = ('name', 'slug')
    list_filter = ('is_active', 'parent')

    inlines = [CategoryMetaTabularInline]

    sortable = 'order'

    class Media:
        js = ['admin/js/category.js']


class AdMetaInline(admin.TabularInline):
    model = AdMeta
    extra = 0


class AdAdmin(admin.ModelAdmin):
    inlines = [AdMetaInline]
    list_display = ('title', 'category', 'slug', 'created_at')
    search_fields = (
        'title', 'description', 'limit-date', 'price', 
        'slug', 'person__name' 'category', 
        'is_active', 'is_bargain', 'view_phone'
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Meta, MetaAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(Offer)
