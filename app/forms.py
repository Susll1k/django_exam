from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import CustomUser,Post,Like
from django.contrib.contenttypes.models import ContentType




class SignUpForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password 1"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password 2"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))

    class Meta:
        model = CustomUser
        fields=['username', 'password1', 'password2', 'email']

class LoginForm(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))

    class Meta:
        model = CustomUser
        fields=['username', 'password']


class CreatePostForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'file-input', 'id':'file-upload'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'title-input',"placeholder": "Title"}))

    class Meta:
        model = Post
        fields = ['title', 'image']
        


class PhotoForm(forms.ModelForm):
    picture = forms.ImageField(widget=forms.FileInput(attrs={'class':'file-input', 'id':'file-upload'}))

    class Meta:
        model = CustomUser
        fields = ['picture']