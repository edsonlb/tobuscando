# coding: utf-8
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse as r
from django.template import loader
from django.contrib.auth import login, authenticate
from django.views.generic import View, TemplateView, DetailView
from django.template.loader import render_to_string
from .models import Ad, AdMeta, Category
from tobuscando.core.forms import PersonPreRegisterForm
from .forms import AdForm, OfferForm, CategoryMetaInlineFormset

import simplejson

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
        if request.user.is_authenticated():
            form_person = self.form_person_class(request.POST)

        if request.POST.get('category'):
            category = Category.objects.get(pk=request.POST.get('category'))
            meta_inlineformset = self.meta_inlineformset_class(request.POST,
                                                               instance=category)

        if form_ad.is_valid() and meta_inlineformset.is_valid():
            if not request.user.is_authenticated():
                if form_person.is_valid():
                    person = form_person.save(commit=False)
                    person.set_password(person.password)
                    person.is_active = True
                    person.save()

                return render(request, self.template_name, locals())
            else:
                person = request.user

            ad = form_ad.save(commit=False)
            ad.person = person
            ad.save()

            for data in meta_inlineformset.cleaned_data:
                AdMeta.objects.create(ad=ad,
                                      meta=data['id'],
                                      option=data['options'])

            request.session['ad_pk'] = ad.pk

            self._login(request, person)
            return redirect(r('ads:ad_success'), ad=ad.pk)

        return render(request, self.template_name, locals())

    def _set_admeta(self):
        pass

    def _login(self, request, person):
        user = authenticate(username=person.username, password=person.password)
        if user is not None:
            if user.is_active:
                login(request, user)


class AdCreateSuccessTemplateView(TemplateView):
    template_name = "ad_success.html"

    def get_context_data(self, **kwargs):
        context = super(AdCreateSuccessTemplateView, self)\
            .get_context_data(**kwargs)

        try:
            context['ad'] = get_object_or_404(Ad,
                                              pk=self.request.session['ad_pk'])
            del self.request.session['ad_pk']
        except:
            context['ad'] = get_object_or_404(Ad, pk=4)

        return context


class AdDetailView(DetailView):
    template_name = 'ad_detail.html'
    model = Ad

    def get_context_data(self, **kwargs):
        context = super(AdDetailView, self).get_context_data(**kwargs)
        context['form_offer'] = OfferForm(initial={
            'ad': self.object.pk,
            'person': self.request.user.pk
        })

        return context


class OfferCreateView(View):
    template_name = 'form_offer_snnipet.html'
    form_class = OfferForm

    def post(self, request, *args, **kwargs):
        form_offer = self.form_class(request.POST)

        if form_offer.is_valid():
            offer = form_offer.save()

            message = u'Sua oferta foi enviada com sucesso. \
                        Aguarde retorno do anunciante.'

            html = loader.render_to_string(self.template_name, {
                'form_offer': self.form_class(initial={
                    'ad': offer.ad.pk,
                    'person': request.user.pk
                }),
                'message': message
            })

            return HttpResponse(simplejson.dumps({'html': html}))

        return render(request, self.template_name, locals())


class CategoryMetaView(View):
    template_name = 'categorymeta_form.html'
    meta_inlineformset_class = CategoryMetaInlineFormset

    def get(self, request, *args, **kwargs):
        category = Category.objects.get(pk=kwargs.get('pk'))

        meta_inlineformset = self.meta_inlineformset_class(instance=category)

        if request.is_ajax():
            return HttpResponse(render_to_string(self.template_name, locals()))

        return render(request, self.template_name, locals())
