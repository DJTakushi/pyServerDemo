from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from django.views.generic import TemplateView
import os
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
def dblog(request):
    template = loader.get_template('dblog/dblogDjango/index.html')
    context = {}
    return HttpResponse(template.render(context,request))
class slugView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        post_name = self.kwargs['slug']
        post_filename = post_name + '.html'
        post_path = os.path.join('dblog/dblogDjango', post_filename)
        print("\n post_path = "+post_path)
        return render(request, post_path)
        # return render(request, post_filename)
class blogPostView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        post_name = self.kwargs['slug']
        post_filename = post_name + '.html'
        year_i = self.kwargs['year']
        month_i = self.kwargs['month']
        day_i = self.kwargs['day']

        year_t = f'{year_i:04}'
        month_t = f'{month_i:02}'
        day_t = f'{day_i:02}'
        post_path = os.path.join('dblog/dblogDjango',year_t,month_t,day_t, post_filename)
        print("\n post_path = "+post_path)
        return render(request, post_path)
        # return render(request, post_filename)
