from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db import transaction



from .constants import ResponseMessage
from .forms import UpdateProfileForm, UpdateUserForm

from allauth.account.views import LoginView


# def profile(request, username):
#     if request.method == 'POST':
#         pass

#     user = get_user_model().objects.filter(username=username).first()
#     if user:
#         form = UpdateUserForm(instance=user)
#         return render(request, 'user/profile.html', context={'form': form})
#     return redirect('home')

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'account/change_password.html'
    success_message = "Successfully Changed Your Password"
    # success_url = reverse_lazy('user-home')
    success_url = reverse_lazy('user-home')

@login_required
def profile(request, username):
    if request.method == 'POST':
        user = request.user
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('profile', user_form.username)
        else:
            user_form = UpdateUserForm(instance=request.user)
            profile_form = UpdateProfileForm(instance=request.user.profile)

        return render(request, 'account/profile.html', {'user_form': user_form, 'profile_form': profile_form})
    
    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UpdateUserForm(instance=user)
        return render(request, 'account/profile.html', context={'form': form})
    return redirect('home')

class UserLoginView(ObtainAuthToken):

    """
    def get(self, request, *args, **kwargs):
         Login page for user

        """

    def post(self, request, *args, **kwargs):
        """ Checks for the login details of the user and sends the Token if successfully authenticated.

        Overrides the default token Authentication View for customized responses.

        """
        serializer = self.serializer_class(data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response(data=ResponseMessage.INVALID_LOGIN_DATA, status=HTTP_401_UNAUTHORIZED)
        else:
            user = serializer.validated_data['user']
            token = Token.objects.get(user=user)
            return Response(data={'token': token.key}, status=HTTP_200_OK)


class UserRegisterView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """Creates a new user and generates their Token with the provided email and password.

        """
        try:
            email = request.data['email']
            password = request.data['password']
        except KeyError:
            return Response(data=ResponseMessage.INVALID_REGISTRATION_KEY, status=HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=email).exists():
            return Response(data=ResponseMessage.ALREADY_REGISTERED, status=HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            user = User.objects.create_user(username=email, email=email, password=password)
            Token.objects.create(user=user)
            return Response(data={'id': user.id, 'username': user.username}, status=HTTP_201_CREATED)