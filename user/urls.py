from django.urls import include, path
from django.conf.urls.static import static
from .views import UserLoginView, UserRegisterView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login.html'),
    path('register/', UserRegisterView.as_view(), name='register')
] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)