import json
from django.shortcuts import render
from django.views import generic
from .models import Basesite, Celllocation

class IndexView(generic.ListView):
    template_name = 'bsites/index.html'
    context_object_name = 'bp'

    def get_queryset(self):
        return Basesite.objects.filter(lac=44677)


class CiView(generic.ListView):
    template_name = 'bsites/lacci.html'
    context_object_name = 'bp'

    def get_queryset(self):
        return Basesite.objects.filter(lac=35001, ci1=145069592).order_by('latitude', 'longitude')


class CilocView(generic.ListView):
    template_name = 'bsites/ciloc.html'
    context_object_name = 'bp'

    def get_queryset(self):
        return Celllocation.objects.filter(lac=35001, ci1=145069592).order_by('latitude', 'longitude')