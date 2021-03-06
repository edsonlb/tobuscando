# coding: utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import View, TemplateView
from django.core.urlresolvers import reverse as r
from django.contrib import messages
from django.utils.translation import ugettext as _
from tobuscando.ads.models import Ad, AdMeta, Offer
from tobuscando.ads.forms import AdUpdateForm, CategoryMetaInlineFormset
from .forms import OfferResponseForm, ProfileForm
from tobuscando.core.models import Person
from django.core.mail import EmailMultiAlternatives

class DashboardView(TemplateView):
    template_name = "dashboard/index.html"


class DashboardAdsView(TemplateView):
    template_name = "dashboard/ad_list.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardAdsView, self).get_context_data(**kwargs)
        context['ads'] = self.request.user.ads()

        return context


class OfferView(TemplateView):
    template_name = "dashboard/offer_list.html"

    def get_context_data(self, **kwargs):
        context = super(OfferView, self).get_context_data(**kwargs)
        context['offers_give'] = self.request.user.offers_give()

        return context

class OfferViewReceive(TemplateView):
    template_name = "dashboard/offer_list_receive.html"

    def get_context_data(self, **kwargs):
        context = super(OfferViewReceive, self).get_context_data(**kwargs)
        context['offers_receive'] = self.request.user.offers_receive()

        return context

''' Edson = Retirei para colocar mais dois quadros na Dashboard.
class OfferView(TemplateView):
    template_name = "dashboard/offer_list.html"

    def get_context_data(self, **kwargs):
        context = super(OfferView, self).get_context_data(**kwargs)
        context['offers'] = self.request.user.offers()

        return context
'''


class OfferResponseView(View):
    template_name = 'dashboard/offer_response_form.html'
    form_class = OfferResponseForm
    success_message = _(u'Oferta respondida com sucesso!')

    def get(self, request, *args, **kwargs):
        offer = Offer.objects.get(pk=kwargs.get('pk'))
        form = self.form_class(initial={
                               'ad': offer.ad.pk,
                               'person': offer.person.pk,
                               'parent': kwargs.get('pk'),
                               'is_active': True
                               })

        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        offer = Offer.objects.get(pk=kwargs.get('pk'))
        form = self.form_class(request.POST)

        offer.is_active = True #request.POST.get('offer_is_active')
        offer.save()

        #envia email para a pessoa que possui o anuncio
        subject = u'Você recebeu uma resposta!'
        from_email = settings.EMAIL_HOST_USER
        to_list = [offer.ad.person.email]
        text_content = u'Voce recebeu uma resposta! Entre no Tobuscando.com e veja!'
        c = Context({
        'username': offer.ad.person.username,
        'url': settings.SITE_URL,
        'url2': offer.ad.get_absolute_url()
        })
        html_content = render_to_string('emails-response/offer_success.html', c)
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        if form.is_valid():
            offer = form.save()

            offer.parent.is_active = True
            offer.parent.save()

            messages.success(self.request, self.success_message)
            return HttpResponseRedirect(r('dashboard:offers_receive_list'))

        return render(request, self.template_name, locals())


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
        meta_inlineformset = self.meta_inlineformset_class(
            instance=ad.category)

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

        if form.is_valid():
            form.save()
            try:
                for data in meta_inlineformset.cleaned_data:
                    try:
                        meta, created = AdMeta.objects.get_or_create(
                            ad=ad, meta=data['id'])
                        meta.option = data['options']
                        meta.save()
                    except:
                        pass
            except:
                        pass

            messages.success(self.request, self.success_message)
            return HttpResponseRedirect(r('dashboard:ad_list'))

        return render(request, self.template_name, locals())


class AdDeleteView(View):
    model = Ad

    def get(self, request, pk):
        ad = get_object_or_404(Ad, pk=pk)
        ad.delete()

        return HttpResponseRedirect(r('dashboard:ad_list'))


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

class ProfileDelete(View):

    def get(self, request):
        person = Person.objects.get(pk=request.user.id)
        person.delete() # Apagar pq o Django não aceita duplicidade de emails, então nao adianta somente o active = False

        return HttpResponseRedirect(r('core:home'))
