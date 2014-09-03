# coding: utf-8
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from random import randint, choice
from django.shortcuts import render
from django.http import HttpResponse

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template.loader import render_to_string

# coding: utf-8
from tobuscando.ads.models import Ad
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialLogin


# Usado para realização de testes na máquina local.
URL = 'http://127.0.0.1:8000/'


from django.dispatch import receiver
from allauth.account.signals import user_signed_up

@receiver(user_signed_up)
def set_attribute(sender, **kwargs):
    user = kwargs.pop('user')
    extra_data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
    social_link = extra_data['link']
    name = extra_data['name']
    first_name = extra_data['first_name']
    last_name = extra_data['last_name']
    email = extra_data['email']
    language = extra_data['locale']
    if language == 'pt_BR':
        user.language = u'Português'
        user.country = 'Brasil'
    else: user.language = language

    user.facebook_link = social_link
    user.name = name
    user.first_name = first_name
    user.last_name = last_name

    user.save()

    #try to send welcome email
    subject = 'Bem vindo ao TôBuscando!'
    from_email = settings.EMAIL_HOST_USER
    to_list = [email, settings.EMAIL_HOST_USER]
    to = email
    text_content = 'Obrigado por entrar em contato. Em breve teremos muitas novidades!'
    html_content = render_to_string('welcome.html', {'equipe':'tobuscando'})
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])       
    msg.attach_alternative(html_content, "text/html")
    msg.send()

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        rand_imagem = randint(1, 4)
        rand_video = ['103562276', '103229541', '103229540', '103229539']

        context['rand_imagem'] = rand_imagem
        context['rand_video'] = choice(rand_video)

        return context


class SearchView(ListView):
    template_name = 'search_list.html'
    model = Ad

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        try:
            context['slug'] = self.get_slug(self.kwargs.get('slug'))
        except:
            pass

        return context

    def get_queryset(self):
        slug = self.get_slug(self.kwargs.get('slug'))
        return self.model.objects.filter(Q(title__icontains=slug) |
                                         Q(description__icontains=slug) |
                                         Q(category__name__icontains=slug))

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
        html_content = render_to_string('email-marketing.html', {'equipe':'tobuscando'})
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])       
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        #send_mail(subject, message, from_email, to_list, fail_silently=True)"""
        return HttpResponse("ok")
    return render(request, 'contact/contact.html', {'form':form})
