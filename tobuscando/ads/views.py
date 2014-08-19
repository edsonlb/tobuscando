# coding: utf-8
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views.generic import View
from django.template.loader import render_to_string
from .models import Ad, AdMeta, Category
from tobuscando.core.forms import PersonPreRegisterForm
from .forms import AdForm, CategoryMetaInlineFormset


class AdCreateView(View):
    template_name = "ad_form.html"
    model_class = Ad
    form_class = AdForm
    form_person_class = PersonPreRegisterForm
    meta_inlineformset_class = CategoryMetaInlineFormset
    category_objects = Category.objects\
                               .filter(is_active=True)\
                               .order_by('tree_id', 'lft')

    def get(self, request, *args, **kwargs):
        categories = self.category_objects
        form_ad = self.form_class
        meta_inlineformset = self.meta_inlineformset_class()
        form_person = self.form_person_class()

        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        categories = self.category_objects
        form_ad = self.form_class(request.POST, request.FILES)
        form_person = self.form_person_class(request.POST)

        if request.POST.get('category'):
            category = Category.objects.get(pk=request.POST.get('category'))
            meta_inlineformset = self.meta_inlineformset_class(request.POST,
                                                               instance=category)

        if form_ad.is_valid() and meta_inlineformset.is_valid() \
                and form_person.is_valid():
            ad = form_ad.save()

            return HttpResponse(ad.pk)

            for data in meta_inlineformset.cleaned_data:
                AdMeta.objects.create(ad=ad,
                                      meta=data['id'],
                                      option=data['options'])

            return HttpResponse(meta_inlineformset.data)

        return render(request, self.template_name, locals())

    def _set_admeta(self):
        pass


class CategoryMetaView(View):
    template_name = 'categorymeta_form.html'
    meta_inlineformset_class = CategoryMetaInlineFormset

    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Category, pk=kwargs.get('pk'))
        meta_inlineformset = self.meta_inlineformset_class(instance=category)

        if request.is_ajax():
            return HttpResponse(render_to_string(self.template_name, locals()))

        return render(request, self.template_name, locals())
