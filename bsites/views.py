import json
from django.shortcuts import render
from django.views import generic
from .models import Basesite, Celllocation
import sys
sys.path.append('/home/yh/dev/django/lc/lcsite/utils')
import findcis

class IndexView(generic.ListView):
    template_name = 'bsites/index.html'
    context_object_name = 'bp'

    def get_queryset(self):
        return Basesite.objects.filter(lac=44677)


class CiView(generic.ListView):
    template_name = 'bsites/lacci.html'
    context_object_name = 'bp'

    def get_queryset(self):
        # return Basesite.objects.filter(lac=34623).order_by('latitude', 'longitude')
        return Basesite.objects.filter(lac=34623, ci1=180515085).order_by('latitude', 'longitude')
        # return Basesite.objects.all().order_by('latitude', 'longitude')
        # return Basesite.objects.all()

class CilocView(generic.ListView):
    template_name = 'bsites/ciloc.html'
    context_object_name = 'bp'

    def get_queryset(self):
        # return Celllocation.objects.all()
        # return Celllocation.objects.filter(lac=34623).order_by('latitude', 'longitude')
        return Celllocation.objects.filter(lac=34623, ci1=180515085).order_by('latitude', 'longitude')


def CisView(request):
    point = [float(request.GET.get('lat','')),float(request.GET.get('lon',''))]
    cis = findcis.whichcis(point)
    context = {'cis': cis}
    return render(request, 'bsites/cis.html', context)