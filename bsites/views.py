import json
import datetime
from django.shortcuts import render
from django.views import generic
from .models import Basesite, Celllocation, Lac
import sys
sys.path.append('/Users/yuhai/Downloads/github/lc/utils')
import findcis

def IndexView(request):
    return render(request, 'bsites/index.html')

def CisView(request):
    point = [float(request.GET.get('lat','')),float(request.GET.get('lon',''))]
    cis = findcis.whichcis(point)
    context = {'cis': cis}
    return render(request, 'bsites/cis.html', context)

def CildView(request):
    lac = int(request.GET.get('lac',''))
    ci = int(request.GET.get('ci',''))
    cif = findcis.findci(lac, ci)
    context = {'ci': cif}
    return render(request, 'bsites/ci.html', context)

def LacsView(request):
    point = [float(request.GET.get('lat','')),float(request.GET.get('lon',''))]
    lacs = findcis.whichlacs(point)
    context = {'lacs': lacs}
    return render(request, 'bsites/lacs.html', context)

class CiView(generic.ListView):
    template_name = 'bsites/lacci.html'
    context_object_name = 'bp'

    def get_queryset(self):
        start = datetime.datetime(2020,6,16,0,0,0)
        end = datetime.datetime(2020,6,16,12,40,0)
        # return Basesite.objects.filter(creatTime__range=(start,end))
        # return Basesite.objects.filter(lac=46594).order_by('latitude', 'longitude')
        return Basesite.objects.filter(lac=46594, ci1=192472589).order_by('latitude', 'longitude')
        # return Basesite.objects.all().order_by('latitude', 'longitude')
        # return Basesite.objects.all()

class CilocView(generic.ListView):
    template_name = 'bsites/ciloc.html'
    context_object_name = 'bp'

    def get_queryset(self):
        start = datetime.datetime(2020,6,16,0,0,0)
        end = datetime.datetime(2020,6,16,12,40,0)
        # return Celllocation.objects.filter(creatTime__range=(start,end))
        # return Celllocation.objects.all()
        return Lac.objects.all()
        # return Celllocation.objects.filter(lac=34623).order_by('latitude', 'longitude')
        # return Celllocation.objects.filter(lac=34623, ci1=180515085).order_by('latitude', 'longitude')

class CilView(generic.DetailView):
    template_name = 'bsites/cil.html'
    model = Celllocation

class LacrView(generic.DetailView):
    template_name = 'bsites/lacr.html'
    model = Lac