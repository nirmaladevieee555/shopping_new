from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # ✅ Correct
from django import forms



class CustomUserForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter User Name'}))
    email=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter email adress'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your password'
    ''}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your confirm password'}))
   
    class Meta:
        model=User
        fields=['username','email','password1','password2']