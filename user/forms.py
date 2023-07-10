from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='A valid email address, please.', required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                            widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email']

class UpdateProfileForm(forms.ModelForm):
    # user = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'row': 1}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'row': 1}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'row': 1}))
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'row': 5}))
    # email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'row': 1}))

    class Meta:
        model = Profile
        exclude = ['id']