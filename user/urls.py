from django.urls import include, path
from django.conf.urls.static import static
from .views import UserRegisterView, UserLoginView, ChangePasswordView, profile, register, UpdateProfileView
from django.contrib.auth.views import LogoutView

# app_name = 'account'

urlpatterns = [

    path('register/', register, name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path('profile/<str:username>/', profile, name='profile'),
    path('<int:pk>/update', UpdateProfileView.as_view(),name='update_profile')
]