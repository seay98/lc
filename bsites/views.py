import json
from django.shortcuts import render
from django.views import generic
from .models import Basesite

class IndexView(generic.ListView):
    template_name = 'bsites/index.html'
    context_object_name = 'bp'

    def get_queryset(self):
        return Basesite.objects.filter(lac=44677)


class IcView(generic.ListView):
    template_name = 'bsites/lacic.html'
    context_object_name = 'bp'

    def get_queryset(self):
        return Basesite.objects.filter(lac=34367, ci1=14597381).order_by('latitude', 'longitude')