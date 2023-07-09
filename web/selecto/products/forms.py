from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
import psycopg2
from .models import SelectoUser

class SignUpForm(ModelForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model =  SelectoUser
        fields = ['username', 'email', 'password1', 'password2']
        db_table = 'selecto-users'
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
