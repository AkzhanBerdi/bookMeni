"""
URL configuration for bookMeni project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from calender import views
from user import views as user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('calendar/', include(('calender.urls', 'calender'), namespace='calender')),
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('account/', include('django.contrib.auth.urls'), name='login'),
    path('account/', include('allauth.urls')),
    # path('accounts/signup', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
    path('login/', user.UserLoginView.as_view(), name='login.html'),
]