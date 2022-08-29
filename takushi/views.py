from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.models import User

from django.views.generic import TemplateView
import os
from django.contrib.contenttypes.models import ContentType
from djangoTask.models import todo
from django.contrib.auth.models import Permission, User
import requests
weatherApiKey = os.environ.get('weatherApiKey')

uperms = ['uCreate','uRead','uUpdate','uDelete']
def getTimeFromZone(tzName):
    utc_dt=datetime.now(timezone.utc)
    myZone=pytz.timezone(tzName)
    output = "{}".format(utc_dt.astimezone(myZone).isoformat())
    time = output.split("T")[-1]
    timeList = time.split(":")
    timeOut = timeList[0]+":"+timeList[1]
    output = timeOut
    output2 = output + " " + myZone.zone
    return output

def getCityData(city):
    api_url = "http://api.weatherapi.com/v1/current.json"
    api_url += "?key="+weatherApiKey
    api_url += "&q="+city+"&aqi=yes"
    response = requests.get(api_url)
    responseJSON = response.json()
    return responseJSON

def base(request):
    template = loader.get_template('takushi/base.html')
    context = {}
    return HttpResponse(template.render(context,request))
def index(request, message=None):
    template = loader.get_template('takushi/index.html')
    context = {}
    if message:
        print("message = "+message)
        context['message_t']=message
    cityNameList = ['Osaka','Atlanta','Chicago']
    cityList = []
    for i in cityNameList:
        apiJsonResponse = getCityData(i)
        cityDict_t = {}
        cityDict_t['name']=apiJsonResponse['location']['name']
        if cityDict_t['name'] == "Osaka-Shi": #adjust for wikipedia link
            cityDict_t['name'] = "Osaka"
        localTime = apiJsonResponse['location']['localtime']
        localTime = localTime.split(" ")[-1] # take time, not date
        cityDict_t["localTime"]=localTime
        cityDict_t["temp_c"] = str(apiJsonResponse['current']['temp_c'])
        cityDict_t["temp_f"] = str(apiJsonResponse['current']['temp_f'])
        cityDict_t["humidity"] = str(apiJsonResponse['current']['humidity'])
        cityDict_t["conditionIcon"] = apiJsonResponse['current']['condition']['icon']
        cityList.append(cityDict_t)
    context['cityList'] = cityList
    return HttpResponse(template.render(context,request))
def about(request):
    template = loader.get_template('takushi/about.html')
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
def profile(request, id = None):
    if request.user.is_authenticated:
        user_t = request.user
        if id != None:
            try:
                user_t = get_object_or_404(User, pk=id)
            except:
                msg = "getting user with id "+str(id)+" failed!"
                return HttpResponseRedirect(reverse('indexM', kwargs={'message':msg}))
        context = {}
        context["user_t"] = user_t
        pList = ["add_todo","change_todo","delete_todo","view_todo"]
        if request.user.is_superuser:
            if 'username' in request.POST:
                if user_t.username != request.POST['username']:
                    print("changing username from "+user_t.username+" to "+ request.POST['username'])
                    user_t.username = request.POST['username']
                if user_t.email != request.POST['email']:
                    print("changing email from "+user_t.email+" to "+ request.POST['email'])
                    user_t.email = request.POST['email']
                if user_t.first_name != request.POST['first_name']:
                    print("changing first_name from "+user_t.first_name+" to "+ request.POST['first_name'])
                    user_t.first_name = request.POST['first_name']
                if user_t.last_name != request.POST['last_name']:
                    print("changing last_name from "+user_t.last_name+" to "+ request.POST['last_name'])
                    user_t.last_name = request.POST['last_name']
                for p in pList:
                    permName = "djangoTask."+p
                    p_in = p in request.POST
                    if p_in:
                        if not(user_t.has_perm(permName)):
                            content_type = ContentType.objects.get_for_model(todo, for_concrete_model=False)
                            permission = Permission.objects.get(codename=p,content_type=content_type,)
                            user_t.user_permissions.add(permission)
                            print(permName+" added.")
                    else:
                        if user_t.has_perm(permName):
                            if user_t.is_superuser:
                                print("cannot remove permissions from superuser")
                            else:
                                content_type = ContentType.objects.get_for_model(todo, for_concrete_model=False)
                                permission = Permission.objects.get(codename=p,content_type=content_type,)
                                user_t.user_permissions.remove(permission)
                                print(permName+" removed.")
                user_t.save()
        # refresh user after changes
        user_t = get_object_or_404(User, pk=user_t.id)

        for p in pList:
            contextName = "perm_"+p
            v = "unchecked"
            if user_t.has_perm("djangoTask."+p):
                v = "checked"
            context[contextName]=v
        if user_t.is_superuser:
            context["user_t_is_superuser"]="checked"
        else:
            context["user_t_is_superuser"]="unchecked"

        template = loader.get_template('registration/profile.html')
        return HttpResponse(template.render(context,request))
    else:
        return HttpResponseRedirect(reverse('login'))
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
def usersView(request, message = None):
    user_list = User.objects.all()
    context = {'user_list':user_list}
    if message:
        context['message_t'] = message
    context['userAdmin'] = request.user.has_perm('takushi.add_user')
    template = loader.get_template('registration/users.html')
    return HttpResponse(template.render(context,request))
def createUser(request):
    context = {}
    context['username_t'] = "username"
    context['email_t'] = "email"
    context['password_t'] = "password"
    context['first_name_t'] = "firstname"
    context['last_name_t'] = "lastname"
    context['message_t'] = None
    template = loader.get_template('registration/createUser.html')
    msg = ""
    if 'username_p' in request.POST:
        context['username_t'] = request.POST['username_p']
        context['email_t'] = request.POST['email_p']
        context['password_t'] = request.POST['password_p']
        msg+="creating user_t..."
        user_t = User.objects.create_user(context['username_t'], context['email_t'],context['password_t'])
        msg_t = "created user_t..."
        print(msg_t)
        msg+=msg_t
        user_t.first_name = request.POST['first_name_p']
        context['first_name_t'] = user_t.first_name
        msg_t = "set user_t.first_name..."
        print(msg_t)
        msg+=msg_t

        user_t.last_name = request.POST['last_name_p']
        context['last_name_t'] = user_t.last_name
        msg_t = "set user_t.last_name..."
        print(msg_t)
        msg+=msg_t

        user_t.save()
        msg_t = "saved user_t..."
        print(msg_t)
        msg+=msg_t

        msg_t = "User "+str(user_t.username) + " created."
        msg+=msg_t

        content_type = ContentType.objects.get_for_model(todo, for_concrete_model=False)
        appName = "djangoTask"
        pList = ["add_todo","change_todo","delete_todo","view_todo"]
        for p in pList:
            permission = Permission.objects.get(
                codename=p,
                content_type=content_type,
            )
            pString =appName+"."+p #app anme defined in apps.py name (I think)
            print(user_t.username + " has "+pString+"= "+str(user_t.has_perm(pString)))

            user_t.user_permissions.add(permission)

            # must get updated instace in cach perhttps://docs.djangoproject.com/en/4.0/topics/auth/default/
            user_t = get_object_or_404(User, pk=user_t.id)
            print(user_t.username + " has "+pString+"= "+str(user_t.has_perm(pString)))
        return HttpResponseRedirect(reverse('usersViewM', kwargs={'message':msg}))
    return HttpResponse(template.render(context,request))
def userDelete(request):
    context = {}
    template = loader.get_template('registration/users.html')
    if 'id' in request.POST:
        try:
            id_t = request.POST['id']
            user_t = get_object_or_404(User, pk=id_t)
            print("got user_t: username = " + str(user_t.username))
            if user_t.is_superuser == False:
                user_t.delete()
                msg = "deleted user "+str(user_t.username)
                print(msg)
                context['message'] = msg
            else:
                msg="cannot delete superuser."
        except:
            msg = "failed to delete with ID "+str(id_t)
        context['message'] = msg
    return HttpResponseRedirect(reverse('usersViewM', kwargs={'message':context['message']}))
