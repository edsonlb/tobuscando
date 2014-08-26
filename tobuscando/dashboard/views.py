# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View, TemplateView
from django.core.urlresolvers import reverse as r
from django.contrib import messages
from django.utils.translation import ugettext as _
from tobuscando.ads.models import AdMeta
from tobuscando.ads.forms import AdUpdateForm, CategoryMetaInlineFormset
from .forms import ProfileForm


class DashboardView(TemplateView):
    template_name = "dashboard/index.html"


class DashboardAdsView(TemplateView):
    template_name = "dashboard/ad_list.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardAdsView, self).get_context_data(**kwargs)
        context['ads'] = self.request.user.ads()

        return context


class AdUpdateView(View):
    template_name = 'dashboard/ad_form.html'
    form_class = AdUpdateForm
    meta_inlineformset_class = CategoryMetaInlineFormset
    success_message = _(u'Anúncio alterado com sucesso.')
    not_found_message = _(u'Anúncio não encontrado.')

    def get(self, request, *args, **kwargs):
        try:
            ad = request.user.ad_set.get(pk=kwargs.get('pk'))
        except:
            messages.info(self.request, self.not_found_message)
            return HttpResponseRedirect(r('dashboard:ad_list'))

        form = self.form_class(instance=ad)
        meta_inlineformset = self.meta_inlineformset_class(instance=ad.category)

        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        try:
            ad = request.user.ad_set.get(pk=kwargs.get('pk'))
        except:
            messages.info(self.request, self.not_found_message)
            return HttpResponseRedirect(r('dashboard:ad_list'))

        form = self.form_class(request.POST, request.FILES, instance=ad)
        meta_inlineformset = self.meta_inlineformset_class(request.POST,
                                                           instance=ad.category)

        if form.is_valid() and meta_inlineformset.is_valid():
            form.save()

            for data in meta_inlineformset.cleaned_data:
                meta, created = AdMeta.objects.get_or_create(ad=ad,
                                                             meta=data['id'])
                meta.option = data['options']
                meta.save()

            messages.success(self.request, self.success_message)
            return HttpResponseRedirect(r('dashboard:ad_list'))

        return render(request, self.template_name, locals())


class ProfileView(View):
    template_name = 'dashboard/profile.html'
    form_class = ProfileForm
    success_message = _(u'Dados alterados com sucesso.')

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)

        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES,
                               instance=request.user)

        if form.is_valid():
            person = form.save()

            messages.success(request, self.success_message)
            return HttpResponseRedirect(r('dashboard:dash_home'))

        return render(request, self.template_name, locals())
