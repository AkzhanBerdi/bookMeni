from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from calender import views as calendar_views
from user import views as user_views
from articles import views as articles_views
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
from user.authentication import CustomAuthToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('articles/', include('articles.urls.articles_urls')),
    path('account/', include('allauth.urls')),
    path('calendar/', include('calender.urls')),
    path('user/', include('user.urls')),
    path('gettoken/', CustomAuthToken.as_view())

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)