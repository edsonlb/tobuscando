from django.shortcuts import render
from tobuscando.contacts.forms import ContactForm
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template.loader import render_to_string
# Create your views here.



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
    return render(request, 'contact/contacts.html', {'form':form})
