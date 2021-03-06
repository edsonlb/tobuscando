# coding: utf-8
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse as r
from django.template import loader
from django.contrib.auth import login, authenticate
from django.views.generic import View, TemplateView, DetailView, ListView
from django.template.loader import render_to_string
from django.db.models import Q
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .models import Ad, AdMeta, Category
from tobuscando.core.forms import PersonPreRegisterForm
from .forms import AdForm, OfferForm, CategoryMetaInlineFormset

from datetime import date
import simplejson
from django.template import Context


class AdListView(ListView):
    model = Ad
    template_name = "ad_list.html"
    model = Ad

    def get_context_data(self, **kwargs):
        context = super(AdListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['slug'] = u'Anúncios'

        return context

    def get_queryset(self):
        return self.model.objects.all().order_by('-created_at', '?')


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

        if request.POST.get('category'):
            category = Category.objects.get(pk=request.POST.get('category'))
            meta_inlineformset = self.meta_inlineformset_class(request.POST,
                                                               instance=category)

        if form_ad.is_valid() and meta_inlineformset.is_valid():
            person = request.user
            if not request.user.is_authenticated():
                form_person = self.form_person_class(request.POST)

                if form_person.is_valid():
                    person = form_person.save(commit=False)
                    person.set_password(person.password)
                    person.is_active = True
                    person.save()
                else:
                    return render(request, self.template_name, locals())

            ad = form_ad.save(commit=False)
            ad.person = person
            ad.save()

            for data in meta_inlineformset.cleaned_data:
                if data['options']:
                    AdMeta.objects.create(ad=ad,
                                          meta=data['id'],
                                          option=data['options'])

            request.session['ad_pk'] = ad.pk

            subject = u'Proposta de compra cadastrada!'
            from_email = settings.EMAIL_HOST_USER
            to_list = [person.email, settings.EMAIL_HOST_USER]
            text_content = ''
            #to = user.email
            c = Context({
                'username': request.user.username,
                'url': settings.SITE_URL,
                'url2': ad.get_absolute_url()
                })
            html_content = render_to_string(
                'emails-response/ad_success.html', c)
            msg = EmailMultiAlternatives(subject, text_content, from_email, to_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            self._login(request)
            return redirect(r('ads:ad_success'), ad=ad.pk)

        return render(request, self.template_name, locals())

    def _set_admeta(self):
        pass

    def _login(self, request):
        user = authenticate(username=request.POST.get('username'),
                            password=request.POST.get('password'))
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
        except:
            return HttpResponseRedirect(r('core:home'))

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

    def get_object(self):
        return self.model.objects.get(Q(limit_date__isnull=True) |
                                      Q(limit_date__gte=date.today()),
                                      pk__exact=self.kwargs['pk'])


class OfferCreateView(View):
    template_name = 'form_offer_snnipet.html'
    form_class = OfferForm

    def post(self, request, *args, **kwargs):
        form_offer = self.form_class(request.POST)

        if form_offer.is_valid():
            offer = form_offer.save()

            # ENVIA MSG PARA A PESSOA QUE RECEBEU A OFERTA
            #message = u'Sua oferta foi enviada com sucesso. \
            #            Aguarde o retorno do usuário.'

            #html = loader.render_to_string(self.template_name, {
            #    'form_offer': self.form_class(initial={
            #        'ad': offer.ad.pk,
            #        'person': request.user.pk
            #    }),
            #    'message': message
            #})

            subject = u'Você recebeu uma proposta!'
            from_email = settings.EMAIL_HOST_USER
            to_list = [offer.ad.person.email]
            text_content = u'Voce recebeu uma proposta! Entre no Tobuscando.com e veja!'
            c = Context({
            'username': offer.ad.person.username,
            'url': settings.SITE_URL,
            'url2': offer.ad.get_absolute_url()
            })
            html_content = render_to_string('emails-response/offer_success.html', c)
            msg = EmailMultiAlternatives(subject, text_content, from_email, to_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            # ENVIA MSG PARA A PESSOA QUE FEZ A OFERTA
            subject = u'Você fez uma proposta!'
            from_email = settings.EMAIL_HOST_USER
            to_list = [request.user.email]
            text_content = u'Voce fez uma oferta! Parabens! Acompanhe o link para fechar bons negocios!'
            c = Context({
            'username': request.user.username,
            'url': settings.SITE_URL,
            'url2': offer.ad.get_absolute_url()
            })
            html_content = render_to_string('emails-response/offer_success_ofertafeita.html', c)
            msg = EmailMultiAlternatives(subject, text_content, from_email, to_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return HttpResponse(simplejson.dumps({'ok': 'true', 'html': html}))

        html = loader.render_to_string(self.template_name, locals())
        return HttpResponse(simplejson.dumps({'ok': 'false', 'html': html}))


class CategoryMetaView(View):
    template_name = 'categorymeta_form.html'
    meta_inlineformset_class = CategoryMetaInlineFormset

    def get(self, request, *args, **kwargs):
        category = Category.objects.get(pk=kwargs.get('pk'))

        meta_inlineformset = self.meta_inlineformset_class(instance=category)

        if request.is_ajax():
            return HttpResponse(render_to_string(self.template_name, locals()))

        return render(request, self.template_name, locals())


class CategoryListView(ListView):
    model = Category
    template_name = "category_list.html"


class CategoryDetailView(DetailView):
    model = Category
    template_name = "category_detail.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)

        categories = self.object.get_children()
        q = Q()
        q.add(Q(category=self.object) |
              Q(category__in=self.object.get_children()),
              Q(limit_date__gte=date.today()) |
              Q(limit_date__isnull=True), Q.AND)
        
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price and max_price:
            q.add(Q(price__in=[min_price, max_price]), Q.AND)
        elif min_price:
            q.add(Q(price__gte=min_price), Q.AND)
        elif max_price:
            q.add(Q(price__lte=max_price), Q.AND)

        f = dict()
        for get in self.request.GET.iteritems():
            if get[0].count('meta'):
                meta = get[0].split('_')
                f['metas__option'] = get[1]

        object_list = Ad.objects.filter(q)\
                                .filter(**f)

        order_by = self.request.GET.get('order_by')
        if order_by:
            object_list = object_list.order_by(order_by)

        context.update(locals())
        return context
