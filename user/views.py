from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import get_user_model, login, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db import transaction
from django.views.generic import UpdateView

from .models import Profile
from .constants import ResponseMessage
from .forms import UpdateProfileForm, UpdateUserForm, UserRegistrationForm
from articles.models import Article
from allauth.account.views import LoginView


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            for error in list(form.errors.values()):
                print(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request = request,
        template_name = 'account/register.html',
        context = {'form': form}
    )

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'account/change_password.html'
    success_message = "Successfully Changed Your Password"
    # success_url = reverse_lazy('user-home')
    success_url = reverse_lazy('home')

@login_required
def profile(request, username):

    if username == request.user.username:
        desired_user = request.user
    else:
        desired_user = get_object_or_404(get_user_model(), username=username)
        
    articles = Article.objects.filter(author=desired_user)
    # user_form = UpdateUserForm(instance=request.user)
    profile_form = UpdateProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        # user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            # user_form.save()
            profile_form.save()
            messages.success(request, f'{profile_form} Your profile is updated successfully')
            return redirect('home')

    form = UpdateProfileForm(instance=desired_user)
    form.fields['bio'].widget.attrs = {'rows': 1}
    
    return render(request, 'account/profile.html', context={
        'form': form,
        # 'user_form': user_form,
        'profile_form': profile_form,
        'desired_user': desired_user,
        'articles': articles
        }
    )


class UserLoginView(ObtainAuthToken):

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


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'account/edit_profile.html'
    context_object_name = 'profile_obj'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields.update(self.get_profile_form().fields)
        return form

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.user}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return UpdateProfileForm(**form_kwargs)

    def get_success_url(self):
        # return reverse('account:profile', kwargs={'pk': self.object.pk})
        return reverse('account:profile', kwargs={'username': self.object.user.username})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form, profile_form):
        context = self.get_context_data(form=form, profile_form=profile_form)
        return self.render_to_response(context)

    def test_func(self):
        return self.request.user == self.get_object()

    def get_object(self, queryset=None):
        return self.request.user.profile