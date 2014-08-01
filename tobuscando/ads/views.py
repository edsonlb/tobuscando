# coding: utf-8
from django.shortcuts import render
from django.views.generic import View
from .models import Ad, Category
from .forms import AdForm


class AdCreateView(View):
    template_name = "ad_form.html"
    model_class = Ad
    form_class = AdForm
    category_objects = Category.objects\
                               .filter(is_active=True)\
                               .order_by('tree_id', 'lft')

    def get(self, request, *args, **kwargs):
        form_ad = self.form_class()
        categories = self.category_objects

        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        form_ad = self.form_class(request.POST)
        categories = self.category_objects

        if form_ad.is_valid():
            pass

        return render(request, self.template_name, locals())
