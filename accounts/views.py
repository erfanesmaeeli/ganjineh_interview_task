from typing import Any, Optional
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User
from django.db.models import Q
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import get_template
from django.urls import reverse_lazy
from rest_framework import generics
from rest_framework.permissions import (
    AllowAny,
)
from . serializers import (
    RegisterSerializer,
)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]