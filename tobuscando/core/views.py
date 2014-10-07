# coding: utf-8
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, TemplateView, ListView
from django.db.models import Q
from random import randint, choice
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialLogin
from tobuscando.ads.models import Ad, Category
from django.template import Context
from .models import Person

from datetime import date

# Usado para realização de testes na máquina local.
#URL = 'http://127.0.0.1:8000/'
URL = 'http://www.tobuscando.com/'

from django.dispatch import receiver
from allauth.account.signals import user_signed_up, password_reset, email_confirmed, email_confirmation_sent, password_changed


@receiver(user_signed_up, dispatch_uid="some.unique.string.id.for.allauth.user_signed_up")
def set_attribute(sender, request, **kwargs):
    user = kwargs.pop('user')
    try:
        extra_data = user.socialaccount_set.filter(
            provider='facebook')[0].extra_data
    except Exception:
        extra_data = None
    if extra_data is not None:
        social_link = extra_data['link']
        name = extra_data['name']
        first_name = extra_data['first_name']
        last_name = extra_data['last_name']
        email = extra_data['email']
        language = extra_data['locale']
        if language == 'pt_BR':
            user.language = u'Português'
            user.country = 'Brasil'
        else:
            user.language = language

        user.facebook_link = social_link
        user.name = name
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # try to send welcome email
        subject = 'Bem vindo ao TôBuscando!'
        from_email = settings.EMAIL_HOST_USER
        to_list = [email, settings.EMAIL_HOST_USER]
        to = email
        text_content = ''
        c = Context({
                'username': user.username
                })
        html_content = render_to_string('welcome.html', c)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return HttpResponseRedirect('/dashboard/')
    else:
        subject = 'Bem vindo ao Tobuscando!'
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email, settings.EMAIL_HOST_USER]
        to = user.email
        text_content = 'Obrigado por entrar em contato. Em breve teremos muitas novidades!'
        html_content = render_to_string(
            'welcome.html', {'equipe': 'tobuscando'}
        )
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return HttpResponseRedirect('/accounts/confirm-email/')

@receiver(password_reset)
def password_reset(sender, request, **kwargs):
    print 'Redirect to url'

#@receiver(email_confirmed)
#def to_email(sender, request, **kwargs):
#    print 'Redirect to url'

#@receiver(email_confirmation_sent)
#def do_you_confirmed(sender, **kwargs):

@receiver(password_changed)
def change_your_pass(sender, user, **kwargs):
    subject = 'Senha alterada com sucesso!'
    from_email = settings.EMAIL_HOST_USER
    to_list = [user.email, settings.EMAIL_HOST_USER]
    to = user.email
    text_content = ''
    c = Context({
            'username': user.username
            })
    html_content = render_to_string('account/email/changed_pass.txt', c)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print user.email

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        rand_imagem = randint(1, 4)
        # https://vimeo.com/tobuscando/videos

        rand_video = ['105236559','103562276','103229541','103229540', '106585219'] #103229539 (Video do Hotsite - Retirado)

        context['rand_imagem'] = rand_imagem
        context['rand_video'] = choice(rand_video)

        return context


class SearchView(ListView):
    template_name = 'search_list.html'
    model = Ad

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        try:
            context['slug'] = self.get_slug(self.kwargs.get('slug'))
        except:
            pass

        return context

    def get_queryset(self):
        keyword = self.get_slug(self.kwargs.get('slug'))
    
        object_list = self.model.objects.filter(Q(title__icontains=keyword) | 
                                                Q(description__icontains=keyword) |
                                                Q(slug__icontains=keyword) |
                                                Q(category__name__icontains=keyword) |
                                                Q(category__slug__icontains=keyword),
                                                Q(limit_date__gte=date.today()) |
                                                Q(limit_date__isnull=True))
    
        order_by = self.request.GET.get('order_by')
        if order_by:
            object_list = object_list.order_by(order_by)
    
        return object_list

    def get_slug(self, slug):
        if not slug:
            return None

        if slug.count('-'):
            return slug.replace('-', ' ')

        return slug

def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid() and request.is_ajax():
        save_it = form.save(commit=False)
        save_it.save()
        subject = 'Chegou a vez do cliente!'
        from_email = settings.EMAIL_HOST_USER
        to_list = [save_it.email, settings.EMAIL_HOST_USER]
        to = save_it.email
        text_content = 'Obrigado por entrar em contato. Em breve teremos muitas novidades!'
        c = Context({
                'username': request.user.username,
                })
        html_content = render_to_string(
            'email-marketing.html', c)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        # send_mail(subject, message, from_email, to_list,
        # fail_silently=True)"""
        return HttpResponse("ok")
    return render(request, 'contact/contact.html', {'form': form})


class PersonAdView(View):
    model = Person
    template_name = "person_view.html"

    def get(self, request, *args, **kwargs):
        print kwargs.get('username')
        person = get_object_or_404(Person, username=kwargs.get('username'))

        return render(request, self.template_name, locals())
