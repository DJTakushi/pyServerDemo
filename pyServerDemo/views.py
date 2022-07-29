from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

def base(request):
    template = loader.get_template('pyServerDemo/base.html')
    context = {}
    return HttpResponse(template.render(context,request))
def index(request):
    template = loader.get_template('pyServerDemo/index.html')
    context = {}
    return HttpResponse(template.render(context,request))
def about(request):
    template = loader.get_template('pyServerDemo/about.html')
    context = {}
    return HttpResponse(template.render(context,request))
