"""takushi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
# import djangoTask.views
from  . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('', views.index, name="takushiIndex"),
    path('index/<str:message>', views.index, name='indexM'),
    path('base', views.base, name="base"),
    path('about', views.about, name="about"),
    path('todo/', include('djangoTask.urls')),
    path('admin/', admin.site.urls, name = "admin"),
    path('dblog',views.dblog, name="dblog"),
    path('dblog/',views.dblog, name="dblog"),
    path('dblog/<slug:slug>.html',views.slugView.as_view()),
    path('dblog/<slug:slug>',views.slugView.as_view()),
    path('dblog/<int:year>/<int:month>/<int:day>/<slug:slug>.html',views.blogPostView.as_view()),
    path('neatApi/',include('neatApi.urls')),
]

urlpatterns += [
    path('accounts/logout/', views.logout_view, name="logout"),
    path('createUser', views.createUser, name="createUser"),
    path('userDelete', views.userDelete, name="userDelete"),
    path('usersView', views.usersView, name="usersView"),
    path('usersView/<str:message>', views.usersView, name="usersViewM"),
    path('user/<int:id>', views.profile, name="user"),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    path('accounts/profile/', views.profile, name="profile"),
    # path('app_list', views.app_list, name="app_list"),

]
