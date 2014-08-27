from django.shortcuts import render
from tobuscando.contacts.forms import ContactForm
from django.http import HttpResponse

# Create your views here.

def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid() and request.is_ajax():
        save_it = form.save(commit=False)
        save_it.save()
        """
        subject = 'Chegou a vez do cliente!'
        from_email = settings.EMAIL_HOST_USER
        to_list = [save_it.email, settings.EMAIL_HOST_USER]
        to = save_it.email
        text_content = 'Obrigado por entrar em contato. Em breve teremos muitas novidades!'
        html_content = "<p align='center'>Acesse nosso <a href='www.tobuscando-landing.herokuapp.com'>site</a>, compartilhe!</p>"+\
                        "<img src='https://lh5.googleusercontent.com/OSbVN7hlNwoVbwbvCr9W95lG5umutIgukoEdXcL6UMY_XZuKQS8YD4nSWPzhBubb_LNn1w=w1290-h536' width='200'></img>"
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        #send_mail(subject, message, from_email, to_list, fail_silently=True)"""

        return HttpResponse("ok")
    return render(request, 'contact/contacts.html', {'form':form})
