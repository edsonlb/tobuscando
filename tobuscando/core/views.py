# coding: utf-8
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from tobuscando.core.models import Person
from tobuscando.core.forms import PersonForm, LoginForm

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard/')
    else:
        form = LoginForm()
        return render(request, 'person/login_normal.html', {'form': form})

def login_validate(request):
    login_html = 'person/login_normal.html'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid(): 
            try:
                user = authenticate(username=form.data['username'].upper(), password=form.data['password'].upper())
                if user is not None:
                    if user.is_active:
                        auth_login(request, user)
                        return HttpResponseRedirect('/dashboard/')
                    else:
                        return render(request, login_html, {'form': form, 'msg':_(u'Conta desativada.')})
                else:
                    return render(request, login_html, {'form': form, 'msg':_(u'Login Inválido.')})
            except: 
                return render(request, login_html, {'form': form, 'msg':_(u'Erro de Login! Revise todas as informações e tente novamente.')})   
        else:
            return render(request, login_html, {'form': form, 'msg':_(u'Os dados não são válidos. Revise os campos!')})    
    else:
        form = LoginForm()
        return render(request, login_html, {'form': form, 'msg':_(u'Erro de login.')}) 


def logoff(request):
    logout(request)
    return HttpResponseRedirect('/')

def register_form(request):
    form = PersonForm()
    return render(request, 'person/register_form.html', {'form': form})

def register_validate(request):
    register_html = 'person/register_form.html'

    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid(): 
            try:
                user = User.objects.create_user()
                user.save()
                #user = authenticate(username=form.data['username'].upper(), password=form.data['password'].upper())
                #http://codeshare.io/Bg35C
                #Envia email de validação
            except: 
                return render(request, register_html, {'form': form, 'msg':_(u'Erro de Login! Revise todas as informações e tente novamente.')})   
        else:
            return render(request, register_html, {'form': form, 'msg':_(u'Os dados não são válidos. Revise os campos!')})    
    else:
        form = LoginForm()
        return render(request, login_html, {'form': form, 'msg':_(u'Erro de login.')}) 

def register_authenticate(request): #Autencidar retorno de email.

def register_password(request): #Enviar lembrete de senha por email.

# LOGIN FIM -------------------------------------

@login_required
def dashboard_index(request):
    return render(request, 'person/dashboard_index.html')


