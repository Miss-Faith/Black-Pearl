from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput

def ForbiddenUsers(value):
  forbidden_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root',
  'email', 'user', 'join', 'sql', 'static', 'python', 'delete']
  if value.lower() in forbidden_users:
    raise ValidationError('Invalid name for user, this is a reserverd word.')

def InvalidUser(value):
  if '@' in value or '+' in value or '-' in value:
    raise ValidationError('This is an Invalid user, Do not user these chars: @ , - , + ')

def UniqueEmail(value):
  if User.objects.filter(email__iexact=value).exists():
    raise ValidationError('User with this email already exists.')

def UniqueUser(value):
  if User.objects.filter(username__iexact=value).exists():
    raise ValidationError('User with this username already exists.')

class SignupForm(forms.ModelForm):
  username = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Username'}), max_length=30, required=True,)
  email = forms.CharField(label='',widget=forms.EmailInput(attrs={'placeholder': 'Email'}), max_length=100, required=True,)
  password = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
  confirm_password = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), required=True)

  class Meta:

    model = User
    fields = ('username', 'email', 'password')

  def __init__(self, *args, **kwargs):
    super(SignupForm, self).__init__(*args, **kwargs)
    self.fields['username'].validators.append(ForbiddenUsers)
    self.fields['username'].validators.append(InvalidUser)
    self.fields['username'].validators.append(UniqueUser)
    self.fields['email'].validators.append(UniqueEmail)

  def clean(self):
    super(SignupForm, self).clean()
    password = self.cleaned_data.get('password')
    confirm_password = self.cleaned_data.get('confirm_password')

    if password != confirm_password:
      self._errors['password'] = self.error_class(['Passwords do not match. Try again'])
    return self.cleaned_data

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user')


class NeighbourHoodForm(forms.ModelForm):
    class Meta:
        model = NeighbourHood
        exclude = ('admin',)


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ('user', 'neighbourhood')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('user', 'neighbourhood')