# coding: utf-8
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from random import randint, choice

from tobuscando.ads.models import Ad


# Usado para realização de testes na máquina local.
URL = 'http://127.0.0.1:8000/'


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
        print slug
        return self.model.objects.filter(Q(title__icontains=slug) |
                                         Q(description__icontains=slug) |
                                         Q(category__name__icontains=slug))

    def get_slug(self, slug):
        if not slug:
            return None

        if slug.count('-'):
            return slug.replace('-', ' ')

        return slug
