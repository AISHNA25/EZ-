from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class CustomAuthenticationForm(AuthenticationForm):
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, required=True)
    username = forms.EmailField(label='Email', max_length=254)

    class Meta:
        model = User
        fields = ['user_type', 'username', 'password']


# Signup form
class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_type']


# File upload form
from .models import UploadedFile
class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
