from django.db import models
from django import forms

# Create your models here.
class LoginForm(forms.Form):
	usernameame = forms.CharField(label = 'Your name')
	password = forms.CharField(label = 'Your password', initial = 'password')
