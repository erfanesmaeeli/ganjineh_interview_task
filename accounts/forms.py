# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 erfan esmaeeli
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from . models import User
# ------------------------------ User SignUp ------------------------------
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password1', 'password2')


# ------------------------------ User Login ------------------------------
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "نام کاربری",
                "class": "form-control",
                "title": ""
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "کلمه عبور",
                "class": "form-control",
                "title": ""
            }
        ))