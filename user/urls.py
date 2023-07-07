from django.urls import include, path
from django.conf.urls.static import static
from .views import UserRegisterView, UserLoginView, ChangePasswordView, profile, register
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path('register/', register, name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('passzword-change/', ChangePasswordView.as_view(), name='password_change'),
    path('profile/<username>', profile, name='profile'),
    
]