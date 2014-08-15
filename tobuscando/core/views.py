# coding: utf-8
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.mail import send_mail
from tobuscando.core.models import Person
from tobuscando.core.forms import PersonForm, LoginForm
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm


URL = 'http://127.0.0.1:8000/' #Usado para realização de testes na máquina local.

# OPERACAIONAL --------------------
def email_enviar(email, assunto, corpo):
    corpo = u'%s E-MAIL AUTOMATICO! NAO RESPONDA!' % corpo
    assunto = u'ToBuscando.com - %s' % assunto
    send_mail(assunto, corpo, settings.EMAIL_HOST_USER, [email], fail_silently=False)

def email_token(person):
    token = person.id + settings.SECRET_TOKEN
    email_enviar(person.email, _('Valide seu E-mail.'), _('<h1>VALIDE SEU EMAIL CLICANDO NO LINK!</h1>%sregister/%s/activate/' % (URL, token)))

def register_activate(request, token):
    if token:
        try:
            token = int(token) - settings.SECRET_TOKEN
            person = Person.objects.get(pk=token, validation=False)
            person.validation = True
            person.is_active = True
            person.save()
            return HttpResponseRedirect('/activation_success/')
        except:
            return HttpResponseRedirect('/activation_error/')

# FIM OPERACIONAL -----------------

# ROTAS --------------------
def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard/')
    else:
        form = LoginForm()
        return render(request, 'person/login_normal.html', {'form': form})

def logoff(request):
    logout(request)
    return HttpResponseRedirect('/')

def register_form(request):
    form = PersonForm()
    return render(request, 'person/register_form.html', {'form': form})

def register_activation_success(request):
    msg = {'alert': 'alert-success', 'msg_top': _(u'Sucesso!'), 'msg': _(u'Você validou o seu registro com sucesso! Agora você já pode realizar o Login!')}
    return render(request, 'person/register_msg.html', {'msg': msg})

def register_activation_error(request):
    msg = {'alert': 'alert-danger', 'msg_top': _(u'Erro!'), 'msg': _(u'Houve um erro de validação! Verifique o link informado no email ou solicite que seja enviado outro email de validação na tela de login.')}
    return render(request, 'person/register_msg.html', {'msg': msg})

def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, template_name='password/password_reset_confirm.html',
        uidb64=uidb64, token=token, post_reset_redirect=reverse('login'))

def reset(request):
    return password_reset(request, template_name='password/password_reset_form.html',
        email_template_name='password/password_reset_email.html',
        subject_template_name='password/password_subject_text.txt',
        post_reset_redirect=reverse('login'))
        #ARRUMAR AQUI!

@login_required
def dashboard_index(request):
    return render(request, 'person/dashboard_index.html')

# FIM ROTAS -----------------

# LOGIN -------------------------------------

def login_validate(request):
    login_html = 'person/login_normal.html'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                user = authenticate(username=form.data['username'].lower(), password=form.data['password'], validation=True)
                if user is not None:
                    if user.is_active:
                        auth_login(request, user)
                        return HttpResponseRedirect('/dashboard/')
                    else:
                        return render(request, login_html, {'form': form, 'msg':_(u'Conta desativada.')})
                else:
                    return render(request, login_html, {'form': form, 'msg':_(u'Login Inválido.')})
            except:
                return render(request, login_html, {'form': form, 'msg':_(u'Erro de Login! Revise todas as informações e tente novamente ou valide primeiro o seu e-mail.')})
        else:
            return render(request, login_html, {'form': form, 'msg':_(u'Os dados não são válidos. Revise os campos!')})
    else:
        form = LoginForm()
        return render(request, login_html, {'form': form, 'msg':_(u'Erro de login.')})

def register_validate(request):
    register_html = 'person/register_form.html'

    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            try:
                person = Person.objects.get(email=form.data['email'].lower()) #verifica se usuário já existe, e se já está validado o email (envia o lembrete de senha)
                msg = {'alert': 'alert-danger', 'msg_top': _('Erro!'), 'msg': _('Já existe uma pessoa cadastrada no sistema com este EMAIL. Faça o login ou peça o lembrete de senha.')}
                return render(request, 'person/register_msg.html', {'msg': msg})
            except:
                person = form.save(commit=False)
                person.set_password(person.password)
                person.save()
                email_token(person)
                msg = {'alert': 'alert-info', 'msg_top': _('Cadastro realizado com Sucesso!'), 'msg': _('Foi enviado um e-mail para <b>'+person.email+'</b>.<br />Valide seu registro clicando no link enviado.')}
                return render(request, 'person/register_msg.html', {'msg': msg})
        else:
            return render(request, register_html, {'form': form, 'msg':_(u'Os dados não são válidos. Revise os campos!')})
    else:
        form = PersonForm()
        return render(request, register_html, {'form': form, 'msg':_(u'Erro de login.')})

# LOGIN FIM -------------------------------------




